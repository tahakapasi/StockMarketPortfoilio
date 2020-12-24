import React, { Component } from "react";
import "./App.css";
import Navbar from "react-bootstrap/Navbar";
import FilterBar from "./Filter.js";
import "bootstrap/dist/css/bootstrap.min.css";
import CompanyList from "./Company";
import axios from "axios";
import { Row, Col, Container } from "react-bootstrap";

class App extends Component {
  state = {
    MinMax: {
      Price: { Min: null, Max: null },
      Volume: { Min: null, Max: null },
      AverageVolume: { Min: null, Max: null },
      PERatio: { Min: null, Max: null },
      MarketCap: { Min: null, Max: null },
      EPS: { Min: null, Max: null },
    },
    FilterParameters: {
      Price: { Min: null, Max: null },
      Volume: { Min: null, Max: null },
      AverageVolume: { Min: null, Max: null },
      PERatio: { Min: null, Max: null },
      MarketCap: { Min: null, Max: null },
      EPS: { Min: null, Max: null },
    },
    Companies: [],
  };

  componentDidMount() {
    this.getMinMax();
    this.fetchCompanyList();
  }

  fetchCompanyList() {
    axios
      .post("http://192.168.29.183:5000/filter", this.state.FilterParameters)
      .then((response) => {
        console.log(response.data.List);
        this.setState({ Companies: response.data.List });
      });
  }

  getMinMax() {
    axios.get("http://192.168.29.183:5000/minmax").then((response) => {
      this.setState({
        MinMax: JSON.parse(JSON.stringify(response.data)),
        FilterParameters: JSON.parse(JSON.stringify(response.data)),
      });
    });
  }

  updateFilterParams(property, value) {
    let newFilterParameters = this.state.FilterParameters;
    newFilterParameters[property] = value;
    this.setState({ FilterParameters: newFilterParameters });
  }

  onSubmit() {
    this.fetchCompanyList();
  }

  render() {
    return (
      <div className="App">
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand>Stock Cart</Navbar.Brand>
        </Navbar>
        <Container fluid>
          <Row>
            <Col md={4} className="bg-light border-right">
              <Container>
                <FilterBar
                  update={this.updateFilterParams.bind(this)}
                  minmax={this.state.MinMax}
                  submit={this.onSubmit.bind(this)}
                />
              </Container>
            </Col>
            <Col md={8}>
              <CompanyList Companies={this.state.Companies} />
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
