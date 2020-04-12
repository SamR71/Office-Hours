import React from 'react';
import {withRouter} from 'react-router-dom';

/* The OfficeHourInfo component displays information about an InstructorOfficeHour object.
 * It displays the information as a string but can be modified. It also handles adding
 * the current office hour to the user's schedule
 */
class OfficeHourInfo extends React.Component {
	// the state holds information from the fields of the InstructorOfficeHour class
	// as well as loggedin to determine the account the user is logged in to
	state = {
		dates: "",
		location: "",
		startTime: "",
        endTime: "",
        loggedin: '',
        instructorName: "",
        instructorType: ""
	};

	constructor(props) {
		super(props);
		this.state = {dates: props.officeHour.meetDates,
					location: props.officeHour.meetLocation,
					startTime: props.officeHour.meetStartTime,
					endTime: props.officeHour.meetEndTime,
					instructorName: props.instructorName,
        			instructorType: props.instructorType,
                    instructor: props.officeHour.meetInstructor};
        // initialize the handleClick function to allow it to execute
        this.handleClick = this.handleClick.bind(this);
	}
    
    // adds the loggedin information to the state
    componentDidMount(){
		var user = localStorage.getItem('loggedinuser');
		this.setState({loggedin: user});
    }

    // adds the current office hour to the schedule of the logged in user
    addToSchedule(){
        // Send POST request to backend to add this office hour object to the user's schedule
        var addURL = 'http://localhost:8000/schedules/add/';
        this.runSendPOSTRequestToBackend(addURL);
    }

    removeFromSchedule(){
        var removeURL = 'http://localhost:8000/schedules/remove/';
        this.runSendPOSTRequestToBackend(removeURL); 
    }

    runSendPOSTRequestToBackend(url){
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                alert(xhr.responseText); // display results of POST request to user
            }
        }
        xhr.onreadystatechange = function() {
        }
        // open a post request at the specified url
        xhr.open('POST', url)
        // create a form with the office hour information
        const form = new FormData()
        form.set('dates', this.state.dates)
        form.set('location', this.state.location)
        form.set('startTime', this.state.startTime)
        form.set('endTime', this.state.endTime)
        form.set('instructor', this.state.instructorName)
        form.set('user',this.state.loggedin)
        // send the form data to the post request
        xhr.send(form)
    }
    
    //executes on the button click to call the addToSchedule() function
	handleClick(event, clickType)
    {
        event.preventDefault();
        if(clickType == "Add"){
            this.addToSchedule();
        }
        else{
            this.removeFromSchedule();
        }

    }

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