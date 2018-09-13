import { connect } from 'react-redux'
import { injectIntl } from 'react-intl';
import { withRouter } from 'react-router'

import { appOperations } from '../../../duck'
import Memberships from './Memberships';


const mapStateToProps = state => 
    ({
        app: state.app,
        loaded: state.shop.school.memberships.loaded,
        memberships: state.shop.school.memberships.data,
        settings: state.app.settings.data
    })

const mapDispatchToProps = dispatch =>
    ({
        setPageTitle(title) {
            dispatch(appOperations.setPageTitle(title))
        }
    })

const MembershipsContainer = withRouter(injectIntl(connect(
    mapStateToProps,
    mapDispatchToProps
)(Memberships)))

export default MembershipsContainer