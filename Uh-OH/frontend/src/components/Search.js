import React from 'react';
import queryString from 'query-string';
import {withRouter} from 'react-router-dom';

class Search extends React.Component {
    state = {
		courses: []
	};
	
	async componentDidMount() {
		try {
			//get url to send to backend
			var url = 'http://localhost:8000/courses/?search=';
			let searchURL = this.props.location.search;
			let params = queryString.parse(searchURL);
			var query = params["course_search_bar"];
			
			//get response, convert to JSON
			const res = await fetch(url+query);
			const coursesjson = await res.json();
			
			//set state
			this.setState({
				courses: coursesjson
			});
		} catch (e) {
			console.log(e);
		}
	}
	
	render() {

        return (
            <div>
				{this.state.courses.map(item => (
					<div key={item.id}>,
						<button type="button" class="btn btn-link" data-toggle="modal" data-target="#exampleModalCenter">
						  <h2>{item.courseName}</h2>
						</button>
						<div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
						  <div class="modal-dialog modal-dialog-centered" role="document">
						    <div class="modal-content">
						      <div class="modal-header">
						        <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
						        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
						          <span aria-hidden="true">&times;</span>
						        </button>
						      </div>
						      <div class="modal-body">
						        ...
						      </div>
						      <div class="modal-footer">
						        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
						        <button type="button" class="btn btn-primary">Save changes</button>
						      </div>
						    </div>
						  </div>
						</div>
						<br></br>
					</div>
				))}
            </div>
        );
    }
}
/**
return (
            <div>
				{this.state.courses.map(item => (
					<div key={item.id}>
						<h2>{item.courseName}</h2>
						<br></br>
					</div>
				))}
            </div>
        );
*/
/**
<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModalCenter">
  Launch demo modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
*/

export default withRouter(Search);