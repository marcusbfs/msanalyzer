import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  cardGrid: {
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(8),
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
  cardMedia: {
    paddingTop: '56.25%', // 16:9
  },
  cardContent: {
    flexGrow: 1,
  },
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(6),
  },
  appBar: {
    marginBottom: '50px',
  },
  mainTab: {
    // backgroundColor: 'red',
  },
  mainTabOptions: {
    // marginTop: '10px',
  },
  execContainer: {
    // marginTop: '40px',
  },
  divider: {
    marginBottom: '30px',
    marginTop: '30px',
  },
  typeDiaRadio: {
    marginTop: '10px',
    marginLeft: '30px',
  },
  ZerosIgnore: {
    marginLeft: '30px',
  },
}));

export default useStyles;
