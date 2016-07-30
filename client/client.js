import React from "react";
import ReactDOM from "react-dom";
var $ = require ('jquery');
var Griddle = require('griddle-react');

var Layout = React.createClass({
    getInitialState: function() {
    return {dataList: []};
    },
    componentDidMount: function() {
        this.serverRequest = $.ajax(
            {
                url: 'http://localhost:5001/updates',
                dataType: 'json',
                cache: false,
                success: function (result) {
                    this.setState({
                        dataList: result
                    });
                }.bind(this)
            }
        );
    },
    render: function() {
        return(
               <Griddle results={this.state.dataList} />
        );
    }
});

const app = document.getElementById('app');

ReactDOM.render(<Layout/>, app);
