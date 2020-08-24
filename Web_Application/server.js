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
var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: true })); 

app.use('/peerjs', peerServer);

app.set('view engine', 'ejs')
app.use(express.static('public'))



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
      }
},{collection: 'users'});

var Users = mongoose.model('Users',UserSchema);

app.get('/login', (req, res) => {
  res.render('login')
})

app.post('/login', (req, res) => {
  var email = req.body.email;
  var password = req.body.password;

  console.log(req.body);

  res.redirect('/login')
})

app.get('/register', (req, res) => {
  res.render('register')
})

app.post('/register', (req, res) => {
  var username = req.body.name;
  var email = req.body.email;
  var contact = req.body.contact;
  var password = req.body.password;
  var confirm_password = req.body.confirm_password;

  

  console.log(req.body);
  

  res.redirect('/register')
})

app.get('/', (req, res) => {
  res.redirect(`/${uuidV4()}`)
})

app.get('/room/:room', (req, res) => {
  res.render('room', { roomId: req.params.room })
})

io.on('connection', socket => {
  socket.on('join-room', (roomId, userId) => {
    socket.join(roomId)
    socket.to(roomId).broadcast.emit('user-connected', userId);
    // messages
    socket.on('message', (message) => {
      //send message to the same room
      io.to(roomId).emit('createMessage', message, userId)
  }); 

    socket.on('disconnect', () => {
      socket.to(roomId).broadcast.emit('user-disconnected', userId)
    })
  })
})



server.listen(process.env.PORT||3030)
