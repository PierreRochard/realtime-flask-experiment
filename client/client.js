import React from "react";
import ReactDOM from "react-dom";
var $ = require ('jquery');
var Griddle = require('griddle-react');
var io = require('socket.io-client');


var Layout = React.createClass({
    getInitialState: function() {
    return {dataList: []};
    },
    componentDidMount: function() {
        var socket = io.connect('/', {
        'reconnection': true,
        'reconnectionDelay': 500,
        'randomizationFactor': 0.5,
        'reconnectionAttempts': 'Infinity'
    });
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
            <div>
               <Griddle results={this.state.dataList} showFilter={true} showSettings={true} />
            </div>
        );
    }
});

const app = document.getElementById('app');

ReactDOM.render(<Layout/>, app);
