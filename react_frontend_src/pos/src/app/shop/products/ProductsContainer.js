import { connect } from 'react-redux'
import { injectIntl } from 'react-intl';
import { withRouter } from 'react-router'

import { appOperations } from '../../duck'
import { shopCartOperations } from '../cart/duck'
import { shopProductsOperations } from './duck'
import { customersListOperations } from '../../customers/list/duck'

import Products from './Products'


const mapStateToProps = state => 
    ({
        app: state.app,
        loaded: state.shop.products.loaded,
        products: state.shop.products,
        products_data: state.shop.products.data
    })

const mapDispatchToProps = dispatch =>
    ({
        setPageTitle(title) {
            dispatch(appOperations.setPageTitle(title))
        },
        addToCart(item) {
            dispatch(shopCartOperations.addItem(item))
        },
        setCustomersListRedirectNext(next) {
            dispatch(customersListOperations.setRedirectNextComponent(next))
        },
        clearSearchTimeout() {
            dispatch(shopProductsOperations.clearSearchTimeout())
        },
        setSearchTimeout(timeout) {
            dispatch(shopProductsOperations.setSearchTimeout(timeout))
        },
        clearSearchValue() {
            dispatch(shopProductsOperations.clearProductsSearchValue())
        },
        setSearchValue(data) {
            dispatch(shopProductsOperations.setProductsSearchValue(data))
        },
        clearSearchProductID() {
            dispatch(shopProductsOperations.clearSearchProductID())
        },
        setSearchProductID(data) {
            dispatch(shopProductsOperations.setSearchProductID(data))
        },
        clearCategoryFilterID() {
            dispatch(shopProductsOperations.clearCategoryFilterID())
        },
        setCategoryFilterID(id) {
            dispatch(shopProductsOperations.setCategoryFilterID(id))
        },

    })

const ProductsContainer = withRouter(injectIntl(connect(
    mapStateToProps,
    mapDispatchToProps
)(Products)))

export default ProductsContainer