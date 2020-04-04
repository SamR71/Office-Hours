import React from 'react';
import {withRouter} from 'react-router-dom';

class OfficeHourInfo extends React.Component {
	state = {
		dates: "",
		location: "",
		startTime: "",
        endTime: "",
        loggedin: ''
	};

	constructor(props) {
		super(props);
		this.state = {dates: props.officeHour.meetDates,
					location: props.officeHour.meetLocation,
					startTime: props.officeHour.meetStartTime,
					endTime: props.officeHour.meetEndTime,
                    instructor: props.officeHour.meetInstructor};
        this.handleClick = this.handleClick.bind(this);
	}
    
    componentDidMount(){
		var user = localStorage.getItem('loggedinuser');
		this.setState({loggedin: user});
    }

    addToSchedule(){
        var url = 'http://localhost:8000/schedules/add/';
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                alert(xhr.responseText);
            }
        }
        xhr.onreadystatechange = function() {
        }
        xhr.open('POST', url)
		const form = new FormData()
		form.set('dates', this.state.dates)
		form.set('location', this.state.location)
        form.set('startTime', this.state.startTime)
		form.set('endTime', this.state.endTime)
        form.set('instructor', this.state.instructor)
        form.set('user',this.state.loggedin)
        xhr.send(form)
    }
    
	handleClick(event)
    {
        event.preventDefault();
        this.addToSchedule();
    }

	render() {
		return (
			<div>
				{/* The Body Content of the OfficeHourInfo component */}
				{this.state.dates + " | " + this.state.location + " | " + this.state.startTime + "-" + this.state.endTime + " "}
				{/* For more info on customizing and adding functionality:
					https://react-bootstrap.github.io/components/buttons/ */}
				{/* The button to add a specific office hours to the user schedule, currently does nothing */}
				<button onClick={this.handleClick} type="button" class="btn btn-sm btn-outline-primary">Add</button>
			</div>
		);
	}

}
export default withRouter(OfficeHourInfo);