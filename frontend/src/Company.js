import React, { Component } from "react";
import { Card, Row, Col } from "react-bootstrap";

class CompanyList extends Component {
  render() {
    // const company_list = (
    //   <ul>
    //     {this.props.Companies.map((c) => (
    //       <li key={c}>{c}</li>
    //     ))}
    //   </ul>
    // );
    return (
      <div>
        <h1>Company List ({this.props.Companies.length})</h1>
        {this.props.Companies.map((c) => {
          return <CompanyCard key={c.SYM} company={c} />;
        })}
      </div>
    );
  }
}

class CompanyCard extends Component {
  render() {
    return (
      <Card style={{ marginBottom: "5px" }}>
        <Card.Header>
          <Row>
            <Col md={8}>{this.props.company.Name}</Col>
            <Col md={2}>{this.props.company.SYM}</Col>
            <Col md={2}>$ {this.props.company.Price}</Col>
          </Row>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={3}>PE {this.props.company.PERatio}</Col>
            <Col md={3}>Avg. Vol. {this.props.company.AverageVolume}</Col>
            <Col md={3}>EPS {this.props.company.EPS}</Col>
            <Col md={3}>Market Cap ${this.props.company.MarketCap}</Col>
          </Row>
        </Card.Body>
        {/* <Card.Body></Card.Body> */}
      </Card>
    );
  }
}

export default CompanyList;
