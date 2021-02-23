/**
 * script for admin view
 * Jean Louis
 * 10/04/2020
 * 
 * quick water shut off test
 */

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

var intialM; 
var span = 5;
var old;

var intialM2; 
var span2 = 5;
var old2;

/**firbase ref and init */
firebase.initializeApp(config);
const dbRef2 = firebase.database().ref()
const usermtr1 = dbRef2.child('users/user1/plants/p1/sensors/motor');
const usermos1  =dbRef2.child('users/user1/plants/p1/sensors/soilmoisture');

const usermtr2 = dbRef2.child('users/user2/plants/p1/sensors/motor');
const usermos2  =dbRef2.child('users/user2/plants/p1/sensors/soilmoisture');


function watering(){
    //const newM = usermos1.val();
    if(old == intialM){
        usermtr1.set('off');
        console.log('turning water off potential error');
    }

}

usermos1.on('value', function(snapshot) {
    intialM =snapshot.val();
});

let motor = 'off';
usermtr1.on('value', function(snapshot) {
    motor =snapshot.val();
    if(motor == 'on'){
        console.log('watering detected')
        old = intialM;
        setTimeout(watering, 8000);
    }
});







function watering2(){
    //const newM = usermos1.val();
    if(old2 == intialM2){
        usermtr2.set('off');
        console.log('turning water off potential error');
    }

}

usermos2.on('value', function(snapshot) {
    intialM2 =snapshot.val();
});

let motor2 = 'off';
usermtr2.on('value', function(snapshot) {
    motor2 =snapshot.val();
    if(motor2 == 'on'){
        console.log('watering detected')
        old2 = intialM2;
        setTimeout(watering2, 8000);
    }
});










 function getAllsensors(){}
 function getAllUsers(){}
 function getAllplants(){}

 function addNewSensor(){}
 function addNewPlant(){}

 function updateSensor(){}
 function updatePlant(){}

 function updatePlantThresh(){}
 



class User {
     constructor(props){
         this.data =props.data;
         this.plants=props.plants
     }
     getName(){
         return data.name
     }

 }

