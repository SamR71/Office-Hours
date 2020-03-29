import React from 'react';
import OfficeHourInfo from "./OfficeHourInfo";
import {withRouter} from 'react-router-dom';

class InstructorInfo extends React.Component {
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
			newName = newName.substring(9);
		}
		this.state = {type: fullType,
					name: newName,
					email: props.instructor.iEmail,
					officeHours: props.instructor.iOfficeHours};
	}
	
	render() {
		return (
			<div>
			{/* The Body Content of the InstructorInfo */}
			<br></br>
			<b> {this.state.type+ ": " + this.state.name} </b> {this.state.email}
				{/* For all office hours the instructor holds, display them */}
				{this.state.officeHours.map(item => (
					<div key = {item.id}>
						<OfficeHourInfo officeHour={item} />
					</div>
				))}
			</div>
		);
	}

}
export default withRouter(InstructorInfo);