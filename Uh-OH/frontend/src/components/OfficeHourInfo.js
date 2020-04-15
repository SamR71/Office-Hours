import React from 'react';
import {withRouter} from 'react-router-dom';

/* The OfficeHourInfo Component Displays Information About An InstructorOfficeHour Object.
 * It Displays The Information As A String, But Can Be Modified. Further, It Also Handles 
 * Adding/Removing Current Office Hour To/From The User's Schedule.
 */
class OfficeHourInfo extends React.Component {
	//The State holds information from the fields of the InstructorOfficeHour Class
	//as well as loggedin to determine the account the User is logged in to.
	state = {
		dates: "",
		location: "",
		startTime: "",
        endTime: "",
        loggedin: '',
        instructorName: "",
        instructorType: "",
        courseName: ""
	};

	constructor(props) {
		super(props);
		this.state = {dates: props.officeHour.meetDates,
					location: props.officeHour.meetLocation,
					startTime: props.officeHour.meetStartTime,
					endTime: props.officeHour.meetEndTime,
					instructorName: props.instructorName,
        			instructorType: props.instructorType,
                    instructor: props.officeHour.meetInstructor,
                    courseName: props.courseName};
        //Initialize the handleClick Function to allow it to properly execute.
        this.handleClick = this.handleClick.bind(this);
	}
    
    // adds the loggedin information to the state
    componentDidMount(){
		var user = localStorage.getItem('loggedinuser');
		this.setState({loggedin: user});
    }

    //Adds The Current Office Hour To The Schedule Of The Logged In User.
    addToSchedule(){
        //Send POST Request To Backend To Add Office Hour To User's Schedule.
        //That is, it will add iff the Office Hours does not already exist in the User's Schedule.
        var addURL = 'http://localhost:8000/schedules/add/';
        this.runSendPOSTRequestToBackend(addURL);
    }

    //Removes The Current Office Hour To The Schedule Of The Logged In User.
    removeFromSchedule(){
        //Send POST Request To Backend To Remove Office Hour From User's Schedule.
        //That is, it will remove iff the Office Hours exists in the User's Schedule.
        var removeURL = 'http://localhost:8000/schedules/remove/';
        this.runSendPOSTRequestToBackend(removeURL); 
    }

    //Common Helper Function Used By addToSchedule()/removeFromSchedule() 
    //To Send POST Request Data To The Backend.
    runSendPOSTRequestToBackend(url){
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                alert(xhr.responseText); // display results of POST request to user
            }
        }
        //Open A POST Request At The Specified URL.
        xhr.open('POST', url)
        //Create A Form w/ Appropriate Office Hour Information Padded.
        const form = new FormData()
        form.set('dates', this.state.dates)
        form.set('location', this.state.location)
        form.set('startTime', this.state.startTime)
        form.set('endTime', this.state.endTime)
        form.set('instructor', this.state.instructorName)
        form.set('user',this.state.loggedin)
        form.set('courseName', this.state.courseName)
        //Send The Form Data To The POST Request.
        xhr.send(form)
    }
    
    //Executes on the Various Button Clicks 
    //To Call Either The addToSchedule()/removeFromSchedule() Functions.
	handleClick(event, clickType)
    {
        event.preventDefault();
        //Case 1: Add Office Hours
        if(clickType == "Add"){
            this.addToSchedule();
        }
        //Case 2: Remove Office Hours
        if(clickType == "Remove"){
            this.removeFromSchedule();
        }

    }

    //Main Rendering Function For Display Of Buttons:
	render() {
		return (
			<div>
				{/* The Body Content of the OfficeHourInfo component */}
				{this.state.dates + " | " + this.state.location + " | " + this.state.startTime + "-" + this.state.endTime + " "}
				
                {/* For more info on customizing and adding functionality:
					https://react-bootstrap.github.io/components/buttons/ */}
				{/*These Are The Buttons To Add/Remove Instructor Office Hours To The User Schedule */}
				<button onClick={(event) => this.handleClick(event, "Add")} type="button" class="btn btn-sm btn-outline-primary">Add</button>
                {<button onClick={(event) => this.handleClick(event, "Remove")} type="button" class="btn btn-sm btn-outline-primary">Remove</button>}
            </div>
		);
	}

}
export default withRouter(OfficeHourInfo);