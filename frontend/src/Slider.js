import React from "react";
import Slider from "@material-ui/core/Slider";
import {
  withStyles,
  makeStyles,
  Theme,
  createStyles,
} from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Tooltip from "@material-ui/core/Tooltip";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      width: 300 + theme.spacing(3) * 2,
    },
    margin: {
      height: theme.spacing(3),
    },
  })
);
interface Props {
  children: React.ReactElement;
  open: boolean;
  value: number;
}

function ValueLabelComponent(props: Props) {
  const { children, open, value } = props;

  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
      {children}
    </Tooltip>
  );
}

const PrettoSlider = withStyles({
  root: {
    color: "#52af77",
    height: 8,
  },
  thumb: {
    height: 24,
    width: 24,
    backgroundColor: "#fff",
    border: "2px solid currentColor",
    marginTop: -8,
    marginLeft: -12,
    "&:focus, &:hover, &$active": {
      boxShadow: "inherit",
    },
  },
  active: {},
  valueLabel: {
    left: "calc(-50% + 4px)",
  },
  track: {
    height: 8,
    borderRadius: 4,
  },
  rail: {
    height: 8,
    borderRadius: 4,
  },
})(Slider);

function RangeSlider(props) {
  const classes = useStyles();
  const [value, setValue] = React.useState(props.value);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const submitChange = (event, newValue) => {
    props.update(props.name, { Min: newValue[0], Max: newValue[1] });
  };

  return (
    // props.update(props.name, { Min: props.min, Max: props.max });
    <div className={classes.root}>
      <Typography id="range-slider" gutterBottom>
        {props.name}
      </Typography>
      <PrettoSlider
        valueLabelDisplay="on"
        value={value}
        ValueLabelComponent={ValueLabelComponent}
        onChange={handleChange}
        onChangeCommitted={submitChange}
        min={props.min}
        max={props.max}
        name={props.name}
      />
    </div>
  );
}

export default RangeSlider;
