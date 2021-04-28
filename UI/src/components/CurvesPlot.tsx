import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';

import Image from './Image';
import { setSingleSVGfile } from '../redux/App.store';

const CurvesPlot = () => {
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

  return <Image image_source={svg_file} />;
};

export default CurvesPlot;
