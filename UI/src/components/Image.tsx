import React from 'react';

import useStyles from '../styles';

interface ImageTypes {
  image_source: string;
}

const Image = ({ image_source }: ImageTypes) => {
  const classes = useStyles();
  return (
    <div>
      <img src={image_source} className={classes.image}></img>
    </div>
  );
};

export default Image;
