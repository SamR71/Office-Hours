import React from 'react';
import MeetingTime from "./MeetingTime";
import InstructorInfo from "./InstructorInfo";
import {withRouter} from 'react-router-dom';

class SectionModal extends React.Component {
	state = {
		name: "",
		id: "",
		courseMeetingTimes: [],
		instructors: [],
	};
	
	constructor(props) {
		super(props);
		this.state = {name: props.name,
						id: props.section.sectionID,
						courseMeetingTimes: props.section.courseMeetingTimes,
						instructors: props.instructors};
	}

	render() {
		return (
			<div>
				{/* The button for the modal, labeled by the section number */}
				<a class="btn btn-link"
					data-toggle="modal"
					href={"#sectionModal"+this.state.name+this.state.id}
					role="button"
					aria-expanded="false"
					aria-controls={"#sectionModal"+this.state.name+this.state.id}>
					{" Section #" +this.state.id}
				</a>
				<br></br>
				{/* The Modal itself */}
				<div class="modal fade"
					id={"sectionModal"+this.state.name+this.state.id}
					tabindex="-1"
					role="dialog"
					aria-labelledby={"#sectionModal"+this.state.name+this.state.id}
					aria-hidden="true">
					<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							{/* The Modal Header Content */}
							<div class="modal-header">
								<h5 class="modal-title" id={"ModalHeader"+this.state.name+this.state.id}>
									{this.state.name}
									<br></br>
									{"Section #" + this.state.id}
								</h5>
								<button type="button" class="close" data-dismiss="modal" aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
							</div>
							{/* The Modal Body Content */}
							<div class="modal-body">
								{/* Display the meeting times for the classes as MeetingTime components*/}
								{this.state.courseMeetingTimes.map(item => (
									<div key = {item.id}>
										<MeetingTime meeting={item} />
									</div>
								))}
								{/* Display the instructors for the classes as InstructorInfo components*/}
								{this.state.instructors.map(item => (
									<div key = {item.id}>
										<InstructorInfo instructor={item} />
									</div>
								))}
							</div>
							{/* The Modal Footer Content: Holds buttons to interact with the section */}
							<div class="modal-footer">
								<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
								<button type="button" class="btn btn-primary">Add to Schedule</button>
							</div>
						</div>
					</div>
				</div>
				<br></br>
			</div>
		);
	}

}
export default withRouter(SectionModal);
