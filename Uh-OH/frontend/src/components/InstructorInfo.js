import React from 'react';
import OfficeHourInfo from "./OfficeHourInfo";
import {withRouter} from 'react-router-dom';

/* The InstructorInfo Component displays information about an Instructor Object.
 * It displays the information as a string but can be modified. It also uses
 * OfficeHourInfo components to display the current instructor's InstructorsOfficeHours
 */
class InstructorInfo extends React.Component {
	//State holds the fields of an Instructor object, as well as an array of InstructorOfficeHours.
	state = {
		type: "",
		name: "",
		email: "",
		officeHours: "",
		courseName: "",
	};
	
	
	constructor(props) {
		super(props);
		// Change the "P" or "T" that represents the type to a full readable string.
		let fullType = "Professor";
		if(props.instructor.iType == "T"){
			fullType="TA";
		}
		//If the name starts with "Professor", remove it...
		//Used To Extract Instructor Type + Name Separately + Store Separrately.
		//For example, "Professor First Last" becomes just "First Last".
		let newName = props.instructor.iName;
		if(newName.indexOf("Professor") == 0){
			newName = newName.substring(10);
		}
		//Update State Values:
		this.state = {type: fullType,
					name: newName,
					email: props.instructor.iEmail,
					officeHours: props.instructor.iOfficeHours,
					courseName: props.courseName};
    }
    
    //Adds All Office Hours For This Instructor To User Schedule At Once
    addToSchedule(){
    	//Simple For Loop Through All Office Hour Data:
        this.state.officeHours.forEach(function(officehour){
            officehour.addToSchedule()
        })
    }
	
	//Main Rendering For Each Instructor Information + Office Hours:
	//To Be Displayed Under SectionModal From SectionModal.js.
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