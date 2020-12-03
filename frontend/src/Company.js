import React, { Component } from "react";

class CompanyList extends Component {
  render() {
    return (
      <div>
        <h1>Company List ({this.props.Companies.length})</h1>
        <ul>
          {this.props.Companies.map((c) => (
            <li key={c}>{c}</li>
          ))}
        </ul>
      </div>
    );
  }
}

export default CompanyList;
