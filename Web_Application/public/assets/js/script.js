const socket = io('/')
const videoGrid = document.getElementById('video-grid')
const screenShareDiv = document.getElementById('screen-share')
const myPeer = new Peer()
let isScreenShared = false
let myId;
let myVideoStream;
let screenStream;
const myVideo = document.createElement('video')
myVideo.muted = true;
const peers = {}
const screenPeers = {}
navigator.mediaDevices.getUserMedia({
  video: true,
  audio: true
}).then(stream => {
  myVideoStream = stream;
  addVideoStream(myVideo, stream)
  myPeer.on('call', call => {
    if(call.metadata.streamType=='video'){
      peers[call.metadata.caller] = call
    }
    else{
      screenPeers[call.metadata.caller] = call
    }
    call.answer(stream)
    const video = document.createElement('video')
    call.on('stream', userVideoStream => {
      addVideoStream(video, userVideoStream)
      changeVideoDimension(Object.keys(peers).length+1)
    })
    call.on('close', () => {
      video.remove()
    })
  })

  socket.on('user-connected', userId => {
    connectToNewUser(userId, stream)
    if(isScreenShared==true){
      const call = myPeer.call(userId, screenStream, {metadata: {caller: myId, streamType: 'screenSharing'}})
      screenPeers[userId] = call
    }
  })
  // input value
  let text = $("input");
  // when press enter send message
  $('html').keydown(function (e) {
    if (e.which == 13 && text.val().length !== 0) {
      socket.emit('message', text.val());
      text.val('')
    }
  });
  socket.on("createMessage", (message, byUser) => {
    $(".messages").append(`<li class="message"><b>${byUser}</b><br/>${message}</li>`);
    scrollToBottom()
  })
})

socket.on('user-disconnected', userId => {
  if (peers[userId]) peers[userId].close()
})

socket.on('screen-shared', screen => {
  $("#video-grid").hide()
  screenShareDiv.append(screen)
})

socket.on('stop-shared-screen', userId => {
  if (screenPeers[userId]) screenPeers[userId].close()
})

myPeer.on('open', id => {
  socket.emit('join-room', ROOM_ID, id, user_email)
  myId = id
})

function connectToNewUser(userId, stream) {
  const call = myPeer.call(userId, stream, {metadata: {caller: myId, streamType: 'video'}})
  const video = document.createElement('video')
  call.on('stream', userVideoStream => {
    addVideoStream(video, userVideoStream)
  })
  call.on('close', () => {
    video.remove()
  })
  peers[userId] = call
  changeVideoDimension(Object.keys(peers).length+1)
}

function addVideoStream(video, stream) {
  video.srcObject = stream
  video.addEventListener('loadedmetadata', () => {
    video.play()
  })
  videoGrid.append(video)
}

function changeVideoDimension(no) {
  if(no>2){
    for(const vg of videoGrid.getElementsByTagName('video')){
      vg.style.height = '240px'
      vg.style.width = '320px'
    }
  }
}



const scrollToBottom = () => {
  var d = $('.main__chat_window');
  d.scrollTop(d.prop("scrollHeight"));
}


const muteUnmute = () => {
  const enabled = myVideoStream.getAudioTracks()[0].enabled;
  if (enabled) {
    myVideoStream.getAudioTracks()[0].enabled = false;
    setUnmuteButton();
  } else {
    setMuteButton();
    myVideoStream.getAudioTracks()[0].enabled = true;
  }
}

const playStop = () => {
  let enabled = myVideoStream.getVideoTracks()[0].enabled;
  if (enabled) {
    myVideoStream.getVideoTracks()[0].enabled = false;
    setPlayVideo()
  } else {
    setStopVideo()
    myVideoStream.getVideoTracks()[0].enabled = true;
  }
}

const setMuteButton = () => {
  const html = `
    <i class="fas fa-microphone"></i>
    <span>Mute</span>
  `
  document.querySelector('.main__mute_button').innerHTML = html;
}

const setUnmuteButton = () => {
  const html = `
    <i class="unmute fas fa-microphone-slash"></i>
    <span>Unmute</span>
  `
  document.querySelector('.main__mute_button').innerHTML = html;
}

const setStopVideo = () => {
  const html = `
    <i class="fas fa-video"></i>
    <span>Stop Video</span>
  `
  document.querySelector('.main__video_button').innerHTML = html;
}

const setPlayVideo = () => {
  const html = `
  <i class="stop fas fa-video-slash"></i>
    <span>Play Video</span>
  `
  document.querySelector('.main__video_button').innerHTML = html;
}

const leaveMeeting = () => {
  socket.disconnect(true)
}

var displayMediaOptions = {
  video: {
    cursor: 'always'
  },
  audio: true
}
const screen = document.createElement('video')

async function startCapture() {
  try {
    screenStream = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);
    screen.srcObject = screenStream
    screen.addEventListener('loadedmetadata', () => {
      screen.play()
    })
    $("#video-grid").hide()
    screenShareDiv.append(screen)
    isScreenShared = true
    for(let peer in peers){
      if(peers[peer].open){
        const call = myPeer.call(peer, screenStream, {metadata: {caller: myId, streamType: 'screenSharing'}})
        screenPeers[peer] = call
      }
    }

    screenStream.oninactive = () => {
      $("#video-grid").show()
      screenShareDiv.remove(screen)
      socket.emit('stop-screen-share')
      for(let peer in peers){
        screenPeers[peer].close()
      }
      isScreenShared = false
    }
  } catch(err) {
    console.error("Error: " + err);
  }
}

function recordScreen(){
  const stop = document.getElementById('stop')
  const recordedVideo = document.getElementById('recorded-video')
  navigator.mediaDevices.getDisplayMedia(displayMediaOptions)
    .then(stream => {
      let mediaRecorder = new MediaRecorder(stream)
      let chunks = []
      mediaRecorder.start()

      stop.onclick = () => {
        mediaRecorder.stop()
      }

      mediaRecorder.ondataavailable = (e) => {
        console.log('Recording')
        chunks.push(e.data)
      }

      mediaRecorder.onstop = () => {
        console.log('Inactive')
        let blob = new Blob(chunks, {'type': 'video/mp4'})
        chunks = []
        let videoURL = window.URL.createObjectURL(blob)
        recordedVideo.src = videoURL
        // const audio = new Audio(videoURL)
        // console.log(audio.textContent)
      }
    })
}