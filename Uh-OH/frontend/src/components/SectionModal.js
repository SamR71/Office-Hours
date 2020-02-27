import React from 'react';
import {withRouter} from 'react-router-dom';

class SectionModal extends React.Component {
	state = {
		name: "",
		id: "",
		meetingTimes: [],
	};
	
	
	constructor(props) {
		super(props);
		this.state = {name: props.course.courseName,
						id: props.section.sectionID,
						meetingTimes: props.section.meetingTimes};
	}
	
	render() {
		return (
			<div>
				<a class="btn btn-link"
					data-toggle="modal"
					href={"#sectionModal"+this.state.name+this.state.id}
					role="button"
					aria-expanded="false"
					aria-controls={"#sectionModal"+this.state.name+this.state.id}>
					{" Section #" +this.state.id}
				</a>
				<br></br>
				<div class="modal fade"
					id={"sectionModal"+this.state.name+this.state.id}
					tabindex="-1"
					role="dialog"
					aria-labelledby={"#sectionModal"+this.state.name+this.state.id}
					aria-hidden="true">
					<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							<div class="modal-header">
								<h5 class="modal-title" id="exampleModalLongTitle">
									{this.state.name}
									<br></br>
									{"Section #" + this.state.id}
								</h5>
								<button type="button" class="close" data-dismiss="modal" aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
							</div>
							<div class="modal-body">
								{/*this.state.meetingTimes.map(item => (
									<div key={item.id}>
										Test
										{/*item.meetType + " | " +
										 item.meetDates + " | " +
										 item.meetStartTime + " to " + item.meetEndTime////}
									</div>
								))*/}
								Temp
							</div>
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
