import React, { Component } from "react";
import "./App.css";
import Navbar from "react-bootstrap/Navbar";
import FilterBar from "./Filter.js";
import "bootstrap/dist/css/bootstrap.min.css";
import NavbarCollapse from "react-bootstrap/esm/NavbarCollapse";
import CompanyList from "./Company";
import axios from "axios";

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
  }

  fetchCompanyList() {
    axios
      .post("http://192.168.29.183:5000/filter", this.state.FilterParameters)
      .then((response) => {
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
    this.fetchCompanyList();
  }

  render() {
    return (
      <div className="App">
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand>Stock Cart</Navbar.Brand>
          <NavbarCollapse>
            <button class="btn btn-primary" id="menu-toggle">
              Toggle Menu
            </button>
          </NavbarCollapse>
        </Navbar>
        <div className="container-fluid hide-sm">
          <div className="row">
            <div className="col bg-light">
              <div className="container">
                <FilterBar
                  update={this.updateFilterParams.bind(this)}
                  minmax={this.state.MinMax}
                />
              </div>
            </div>
            <div className="col">
              <CompanyList Companies={this.state.Companies} />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
