import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';

import useStyles from '../styles';

import { setSingleSVGfile } from '../redux/App.store';

const CurvesPlot = () => {
  const classes = useStyles();

  const dispatch = useDispatch();

  const isComputing = useSelector((state: RootState) => state.app.isComputing);
  const isSingleMode = useSelector(
    (state: RootState) => state.app.isSingleFile
  );
  const outName = useSelector((state: RootState) => state.app.outName);
  const outDir = useSelector((state: RootState) => state.app.outDirName);
  const svg_file = useSelector((state: RootState) => state.app.singleSVGfile);

  React.useEffect(() => {
    let svg = '';
    if (isSingleMode) {
      svg = outDir + '\\' + outName + '_curves.svg';
    } else {
      svg = outDir + '\\' + outName + '_frequency.svg';
    }
    dispatch(setSingleSVGfile(svg));
  }, [outDir, outName, isComputing, isSingleMode]);

  return (
    <div>
      <img src={svg_file} className={classes.image}></img>
    </div>
  );
};

export default CurvesPlot;
