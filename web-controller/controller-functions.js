// Rosbridge Connection Functions
// ----------------------
var ros = new ROSLIB.Ros({
  url : 'ws://localhost:9090'
});

ros.on('connection', function() {
  console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
  console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
  console.log('Connection to websocket server closed.');
});


var controlsDisabled=true;


// Subscribing to the Current Level Topic
// ----------------------
var listener = new ROSLIB.Topic({
  ros : ros,
  name : '/currentGameLevel',
  messageType : 'std_msgs/String'
});

listener.subscribe(function(message) {
  if (message.data=="PRESS START"){
    document.getElementById("start").innerHTML = message.data;
    document.getElementById("level").style.display="none"
    document.getElementById("start").style.display="block";
  }
  else{
    if(message.data=="GAME OVER") controlsDisabled=true;
    else controlsDisabled=false;
    document.getElementById("level").innerHTML = message.data;
    document.getElementById("start").style.display="none"
    document.getElementById("level").style.display="block";
  }
  
  console.log('Received message on ' + listener.name + ': ' + message.data);
});




// Calling the /start_turtlesim_snake service
// ----------------------
function startSnakeGame(){
  var startGameClient = new ROSLIB.Service({
    ros : ros,
    name : '/start_turtlesim_snake',
    serviceType : 'learning_tf/start_turtlesim_snake'
  });

  var request = new ROSLIB.ServiceRequest({});
  startGameClient.callService(request);
}

// Publishing the /turtle1/cmd_vel Topic
// ------------------
function moveForwards(){
  var cmdVel = new ROSLIB.Topic({
    ros : ros,
    name : 'turtle1/cmd_vel',
    messageType : 'geometry_msgs/Twist'
  });

  var twist = new ROSLIB.Message({
    linear : {
      x : 2.0,
      y : 0.0,
      z : 0.0
    },
    angular : {
      x : 0.0,
      y : 0.0,
      z : 0.0
    }
  });
  if (!controlsDisabled) cmdVel.publish(twist);
}

function moveBackwards(){
  var cmdVel = new ROSLIB.Topic({
    ros : ros,
    name : 'turtle1/cmd_vel',
    messageType : 'geometry_msgs/Twist'
  });

  var twist = new ROSLIB.Message({
    linear : {
      x : -2.0,
      y : 0.0,
      z : 0.0
    },
    angular : {
      x : 0.0,
      y : 0.0,
      z : 0.0
    }
  });
  if (!controlsDisabled) cmdVel.publish(twist);
}

function turnLeft(){
  var cmdVel = new ROSLIB.Topic({
    ros : ros,
    name : 'turtle1/cmd_vel',
    messageType : 'geometry_msgs/Twist'
  });

  var twist = new ROSLIB.Message({
    linear : {
      x : 0.0,
      y : 0.0,
      z : 0.0
    },
    angular : {
      x : 0.0,
      y : 0.0,
      z : 1.0
    }
  });
  if (!controlsDisabled) cmdVel.publish(twist);
}

function turnRight(){
  var cmdVel = new ROSLIB.Topic({
    ros : ros,
    name : 'turtle1/cmd_vel',
    messageType : 'geometry_msgs/Twist'
  });

  var twist = new ROSLIB.Message({
    linear : {
      x : 0.0,
      y : 0.0,
      z : 0.0
    },
    angular : {
      x : 0.0,
      y : 0.0,
      z : -1.0
    }
  });
  if (!controlsDisabled) cmdVel.publish(twist);
}


// Monitoring the arrow keys for turtle movement
// --------------------------
document.onkeydown = checkKey;

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '38') {
        // up arrow
        moveForwards();
    }
    else if (e.keyCode == '40') {
        // down arrow
        moveBackwards();
    }
    else if (e.keyCode == '37') {
       // left arrow
       turnLeft();
    }
    else if (e.keyCode == '39') {
       // right arrow
       turnRight();
    }

}

