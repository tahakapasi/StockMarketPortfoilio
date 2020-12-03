import React, { Component } from "react";
import RangeSlider from "./Slider";

class FilterBar extends Component {
  floatSliders = ["Price"];

  render() {
    return (
      <div class="bg-light border-right" id="sidebar-wrapper">
        <div class="sidebar-heading">Start Bootstrap </div>
        <div class="list-group list-group-flush">
          <div href="#" class="list-group-item list-group-item-action bg-light">
            {this.floatSliders.map((property) => (
              <RangeSlider
                update={this.props.update}
                name="Price"
                min={this.props.minmax[property]["Min"]}
                max={this.props.minmax[property]["Max"]}
              />
            ))}
          </div>
          <a href="#" class="list-group-item list-group-item-action bg-light">
            Shortcuts
          </a>
          <a href="#" class="list-group-item list-group-item-action bg-light">
            Overview
          </a>
          <a href="#" class="list-group-item list-group-item-action bg-light">
            Events
          </a>
          <a href="#" class="list-group-item list-group-item-action bg-light">
            Profile
          </a>
          <a href="#" class="list-group-item list-group-item-action bg-light">
            Status
          </a>
        </div>
      </div>
    );
  }
}

export default FilterBar;
