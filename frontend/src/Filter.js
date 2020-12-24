import React, { Component } from "react";
import RangeSlider from "./Slider";
import { Button, Container } from "react-bootstrap";

class FilterBar extends Component {
  floatSliders = [
    "Price",
    "PERatio",
    "MarketCap",
    "AverageVolume",
    "EPS",
    "Volume",
  ];

  render() {
    return (
      <Container className="bg-light">
        <h3>Filter</h3>
        <div className="list-group list-group-flush">
          {this.floatSliders.map((property) => (
            <div
              key={property}
              className="list-group-item list-group-item-action bg-light"
            >
              <RangeSlider
                update={this.props.update}
                name={property}
                min={this.props.minmax[property]["Min"]}
                max={this.props.minmax[property]["Max"]}
                value={[
                  this.props.minmax[property]["Min"],
                  this.props.minmax[property]["Max"],
                ]}
              />
            </div>
          ))}
          <Button onClick={this.props.submit}>Submit</Button>
        </div>
      </Container>
    );
  }
}

export default FilterBar;
