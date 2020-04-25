import React from "react";
import PropTypes from "prop-types";

const propTypes = {
		start: PropTypes.object.isRequired,
		end: PropTypes.object.isRequired,
		loc: PropTypes.string.isRequired,
	prof: PropTypes.string.isRequired,
};

class customEvent extends React.PureComponent 
{
	render() 
	{
		const {
			start,
			end,
			value,
		} = this.props;
		return (
			<div className="event" style={{textAlign: "center"}}>
				{this.props.prof} <br/> {this.props.loc}
			</div>
		);
	}
}

customEvent.propTypes = propTypes;
export default customEvent;