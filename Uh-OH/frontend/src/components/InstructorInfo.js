import React from 'react';
import OfficeHourInfo from "./OfficeHourInfo";
import {withRouter} from 'react-router-dom';

/* The InstructorInfo component displays information about an Instructor object.
 * It displays the information as a string but can be modified. It also uses
 * OfficeHourInfo components to display the current instructor's InstructorsOfficeHours
 */
class InstructorInfo extends React.Component {
	// the state holds the fields of an Instructor object, as well as an array of InstructorOfficeHours
	state = {
		type: "",
		name: "",
		email: "",
		officeHours: "",
	};
	
	
	constructor(props) {
		super(props);
		// Change the "P" or "T" that represents the type to a full readable string
		let fullType = "Professor";
		if(props.instructor.iType == "T"){
			fullType="TA";
		}
		// if the name starts with "Professor", remove it
		// for example "Professor First Last" becomes "First Last"
		let newName = props.instructor.iName;
		if(newName.indexOf("Professor") == 0){
			newName = newName.substring(10);
		}
		this.state = {type: fullType,
					name: newName,
					email: props.instructor.iEmail,
					officeHours: props.instructor.iOfficeHours};
    }
    
    // Add all office hours for this instructor to the schedule at once
    addToSchedule(){
        this.state.officeHours.forEach(function(officehour){
            officehour.addToSchedule()
        })
    }
	
	render() {
		return (
			<div>
			{/* The Body Content of the InstructorInfo, displays the info as text */}
			<br></br>
			<b> {this.state.type+ ": " + this.state.name} </b> {this.state.email}
				{/* For all office hours the instructor holds, map them to
					OfficeHourInfo components with their ID as the key */}
				{this.state.officeHours.map(item => (
					<div key = {item.id}>
						<OfficeHourInfo officeHour={item} instructorName={this.state.name} instructorType={this.state.type}/>
					</div>
				))}
			</div>
		);
	}

}
export default withRouter(InstructorInfo);