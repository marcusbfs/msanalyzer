import React from 'react';

import useStyles from '../styles';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';

//create your forceUpdate hook
export function useForceUpdate() {
  const [value, setValue] = React.useState(0); // integer state
  return () => setValue((value) => value + 1); // update the state to force render
}

interface ImageTypes {
  image_source: string;
}

const Image = ({ image_source }: ImageTypes) => {
  const isComputing = useSelector((state: RootState) => state.app.isComputing);
  const isSingleMode = useSelector(
    (state: RootState) => state.app.isSingleFile
  );

  const forceUpdate = useForceUpdate();

  const classes = useStyles();
  React.useEffect(() => {
    forceUpdate;
  }, [isComputing, isSingleMode]);

  return (
    <div>
      <img
        src={image_source}
        key={image_source}
        className={classes.image}
      ></img>
    </div>
  );
};

export default Image;
