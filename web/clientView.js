/*
"""
Created on Sun Oct  4 03:29:01 2020
@author: Jean Louis
*/

//var config = require(config.js);
//print(config)
const authuser1 ='user1';
const authuser2 ='user2';
var user='';


// Initialize Firebase 
var config={
    "apiKey": "AIzaSyCc0dbHCJjrlj2BcQ0o1MDfBYIWM-5alHY",
    "authDomain": "smartplant-a4063.firebaseapp.com",
    "databaseURL": "https://smartplant-a4063.firebaseio.com",
    "projectId": "smartplant-a4063",
    "storageBucket": "smartplant-a4063.appspot.com",
    "messagingSenderId": "999668661309",
    "appId": "1:999668661309:web:2221b8685e974d18887e54",
    "measurementId": "G-P796ZSL3HQ"    
}


/**firbase ref and init */
firebase.initializeApp(config);
const dbRef = firebase.database().ref()
const usersRef = dbRef.child('users');
const testRef =dbRef.child("test-DHT")

// users{user1}/plants/p1/sensors

/**get ui elements from doc */
var usernameIn = document.getElementById('user');
var dataList = document.getElementById('plantList')
var check = document.getElementById('check');
var watering =false;
var loggedin = false;
var water = document.getElementById('water');
var testDHT = document.getElementById('testing');

function loaded(){
    removeAllChildNodes(testDHT); 
}
removeAllChildNodes(testDHT);

/**
 * place holder login system only 2 know users
 */
function logIn(){
    removeAllChildNodes(testDHT);
    var username = usernameIn.value;
    if(username == authuser1 || username == authuser2){
        loggedin =true;
        user =username
        const currentUser = getUser(user);
        currentUser.on('value', function(snapshot) {
            updateTest(snapshot.val());
        });
       //showdata(user);
    }
    else{
        loggedin = false;
        usernameIn.value ='';
        removeAllChildNodes(testDHT);
        alert("username invalid")
    }
}

function updateTest(data){
    removeAllChildNodes(testDHT);
    let status = document.createElement('h3');
    let led = document.createElement('h3');
    let humidity = document.createElement('h3');
    let soilcondition = document.createElement('h3');
    let soilmoisture = document.createElement('h3');
    let temp = document.createElement('h3');
    let motor = document.createElement('h3');

    status.innerHTML="The status is: "+data.status;
    led.innerHTML ="The LED is: "+data.sensors.led;
    humidity.innerHTML ="The humidity is: "+data.sensors.humidity;
    soilcondition.innerHTML ="The soild condition is: "+data.sensors.soilcondition;
    soilmoisture.innerHTML ="The moistrue level is: "+data.sensors.soilmoisture;
    temp.innerHTML ="The temp is: "+data.sensors.temp;
    motor.innerHTML ="the motor is: "+data.sensors.motor;

    if(data.sensors.motor == "off"){
        const newState = false;
        water.innerHTML = newState ? '<i>watering</i>':'<i">off</i>';
        watering = newState;
        check.checked =false;
    }

    testDHT.appendChild(status);
    testDHT.appendChild(led);
    testDHT.appendChild(humidity);
    testDHT.appendChild(soilcondition);
    testDHT.appendChild(soilmoisture);
    testDHT.appendChild(temp);
    testDHT.appendChild(motor);
}

function showdata(curruser){
    removeAllChildNodes(dataList)
    var plants = db[curruser].plants
    plants.forEach(renderData)
    
}

function removeAllChildNodes(node) {
    node.querySelectorAll('*').forEach(n => n.remove());
    
    console.log('cleared');
    node.textContent ='';
}


/**update the UI and updates the given actuator */
function enableActuator() { 
    if(user != ''){ 
        const newState = !watering;
        water.innerHTML = newState ? '<i>watering</i>':'<i">off</i>';
        watering = newState;
        if(watering){
            //dbRef.child('users/'+name+'/plants/p1');
        const mtref= getUser(user);
        mtref.child('sensors/motor').set("on"); 
        }
        else{
            const mtref= getUser(user);
        mtref.child('sensors/motor').set("off"); 

        }
    }
  } 

// users{user1}/plants/p1/sensors
function getUser(name){
    return dbRef.child('users/'+name+'/plants/p1');
}


function writeUserData(data) {
    firebase.database().ref('users/').set({data});
}



/**update the UI when new plant is added to user's data base */
function onPlantAdded(user,newplant){}
/** called when propertyies of the plant has changed*/
function onplantUpdate(plant,data){}
/**future use if server updates sensor property */
function onSensorUpdate(sensor,data){}
/**called when the user wants to manually activate an actuator */
function onUserOverWrite(sensor,data){}
/**Does the firbase authentication for user */
function authenticate(user){}
/**generate new token to keep the user logged in */
function updateTokens(){}


/**retrieve a list of planst for this user */
function getPlants(user){
    return db[user].plants();
}
/**retrieve a list of sensors for a given plant */
function getSensorData(plant){
    return plant.sensors;
}







//fier stor class to collection
//https://firebase.google.com/docs/firestore/query-data/get-data#web_1


