const express = require('express')
const app = express()
// const cors = require('cors')
// app.use(cors())
const server = require('http').Server(app)
const io = require('socket.io')(server)
const { ExpressPeerServer } = require('peer');
const peerServer = ExpressPeerServer(server, {
  debug: true
});
const mongoose = require('mongoose');
const { v4: uuidV4 } = require('uuid')

const sha256 = require('js-sha256');
const session = require('express-session');

var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: true })); 

app.use('/peerjs', peerServer);

app.set('view engine', 'ejs')
app.use(express.static('public'))

app.use(session({ 
  secret: "John Wick", 
  resave: false, 
  saveUninitialized: false
}));

mongoose.connect("mongodb+srv://qwerty:qwerty@123@be-project.llqsi.mongodb.net/BE-Project?retryWrites=true&w=majority", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useCreateIndex: true
}).then(() => {
  console.log('Mongo Connection Successful');
}).catch(err => {
  console.log('ERROR:', err.message);
})


var UserSchema = new mongoose.Schema(
  { 
   user_name: {
        type: String,
        require: true
      },
   user_password: {
        type: String,
        require: true
      },
   email:  {
        type: String,
        require: true
      },
    contact: {
      type: String,
      require: true
    }
},{collection: 'users'});

var RoomSchema = new mongoose.Schema(
  { 
   room_id: {
        type: String,
        require: true
      },
   created_by_user: {
        type: String,
        require: true
      },
   active: {
        type: Boolean,
        require: true
      },
    members: [{
      type: String
    }],
    members_attended: [{
      type: String
    }]
},{collection: 'rooms'});

var Users = mongoose.model('Users',UserSchema);
var Rooms = mongoose.model('Rooms', RoomSchema);

const redirectLogin = (req, res, next) => {
  if (!req.session.email){
    res.redirect('/login');
  }
  else{
    next();
  }
}

app.get('/login', (req, res) => {
  res.render('login', { message: "", message_category: 'danger' })
})

app.post('/login', (req, res) => {
  var email = req.body.email;
  var password = req.body.password;

  Users.findOne({email: email, user_password: sha256(password)}, (err, data) => {
    if (err) {
      console.log(err);
      res.render('login', { message: "Something went wrong !!!", message_category: 'danger' });
    }
    else{
      if(data == null){
          res.render("login", {message: "Invalid Email or Password !!!", message_category: 'danger'});
      }
      else{
        // User exits
        console.log(data);
        req.session.user = data;
        req.session.email = email;
        req.session.name = data.user_name;
        res.redirect('/');
      }
    }
  });

})

app.get('/logout', redirectLogin, (req, res) => {
  req.session.destroy(err => {
    if (err) {
      res.redirect('/')
    }
    else{
      res.redirect('/login')
    }
  })
})

app.get('/register', (req, res) => {
  res.render('register', { message: "", message_category: 'danger' });
})

app.post('/register', (req, res) => {
  var name = req.body.name;
  var email = req.body.email;
  var contact = req.body.contact;
  var password = req.body.password;
  var confirm_password = req.body.confirm_password;

  // check if user already exists
  Users.findOne({email: email}, (err, data) => {
    if (err) {
      console.log(err);
      res.render('register', { message: "Something went wrong !!!", message_category: 'danger' });   
    }
    else{
      if(data == null){
        // no user with this email make new one
        if (password != confirm_password){
          res.render('register', { message: "Passwords does not match.", message_category: 'danger' }); 
        }
        else{
          Users.create(
            {
              user_name: name,
              user_password: sha256(password),
              email: email,
              contact: contact 
            },
            function (err, Users) {
              if (err) {
                console.log(err);
              }
              else {
                console.log(Users);
              }
            }
          );
          res.render("login", { message: "User Created Successfully.", message_category: 'success'});
        }
      }
      else{
        // User already exits
        res.render('register', { message: "User already exists.", message_category: 'danger'}); 
      }
    }
  });
})

app.get('/', redirectLogin, (req, res) => {
  var user = req.session.user;
  res.render('home', {user: user})
})

app.get('/create-room', redirectLogin, (req, res) => {

  var room_id = uuidV4();

  Rooms.create(
    {
      room_id: room_id,
      created_by_user: req.session.email,
      active: true,
      members: [],
      members_attended: []
    }
  );

  res.redirect(`/room/${room_id}`)
})


app.get('/room/:room', redirectLogin, (req, res) => {
  var user = req.session.user;

  var room_id = req.params.room;

  Rooms.findOne({room_id: room_id, active:true}, (err, room) => {
    if (err) {
      console.log(err);
      res.redirect('/');
    }
    else{
      if ( room != null) { 
        res.render('room', { roomId: room_id, user: user })        
      }
      else{
        res.redirect('/');
      }
    }
  });
})

io.on('connection', socket => {
  socket.on('join-room', (roomId, userId, email) => {
    
    socket.join(roomId);
    socket.to(roomId).broadcast.emit('user-connected', userId);

    Rooms.findOne({room_id: roomId, active:true}, (err, data) => {
      if (err) {
        console.log(err);
      }
      else{
        if(data != null){
          console.log(data);
          var members = data.members;
          var members_attended = data.members_attended;
          members.push(email);
          members_attended.push(email);
          data.members = members;
          data.members_attended = members_attended;
          data.save();
        }
        else{
          console.log('No such room');
        }
      }
    });

    // messages
    socket.on('message', (message) => {
      //send message to the same room
      io.to(roomId).emit('createMessage', message, userId)
    }); 

    socket.on('disconnect', () => {

      Rooms.findOne({room_id: roomId}, (err, data) => {
        if (err) {
          console.log(err);
        }
        else{
          if(data != null){
            console.log(data);
            var members = data.members;
            var i = members.indexOf(email);
            members.splice(i, 1);
            data.members = members;
            if (data.members.length == 0){
              data.active = false;
            }
            data.save();
          }
          else{
            console.log('No such room');
          }
        }
      });

      socket.to(roomId).broadcast.emit('user-disconnected', userId)
    })

    socket.on('stop-screen-share', () => {
      socket.to(roomId).broadcast.emit('stop-shared-screen', userId)
    })
  })
})



server.listen(process.env.PORT||3030)
