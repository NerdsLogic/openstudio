import {
    requestCustomers,
    receiveCustomers,
    requestCreateCustomer,
    receiveCreateCustomer,
    requestUpdateCustomer,
    receiveUpdateCustomer,
    requestSaveCameraAppSnap,
    receiveSaveCameraAppSnap,
    setCreateCustomerStatus,
    setUpdateCustomerStatus,
    setSearchTimeout,
    clearSearchTimeout,
    setDisplayCustomerID,
    clearDisplayCustomerID,
    setSearchCustomerID,
    clearSearchCustomerID,
    setSearchValue,
    clearSearchValue,
    setSelectedCustomerID,
    clearSelectedCustomerID,
    setRedirectNextComponent,
    clearRedirectNextComponent,
    setCameraAppSnap,
    clearCameraAppSnap
} from './actions'

import axios_os from '../../../../utils/axios_os'
import OS_API from '../../../../utils/os_api'

// just pass these actions as there's nothing else they need to do
// Put pass-through actions here
// const setCheckinClassAttendanceSearchCustomerID = set_customer_id

// data fetchers
const fetchCustomers = () => {
      return dispatch => {
          dispatch(requestCustomers())

          axios_os.get(OS_API.CUSTOMERS)
          .then(function (response) {
            // handle success
            dispatch(receiveCustomers(response.data))
            // dispatch(setLoadingProgress(100))
          })
          .catch(function (error) {
            // handle error
            console.log(error)
          })
          .then(function () {
            // always executed
          });
      }
  }

// helpers
const formDataToObject = (fd_obj) => {
    const data_object = {}

    for (var p of fd_obj) {
        console.log(p)
        data_object[p[0]] = p[1]
    }

    return data_object
}

// creators
const createCustomer = (data) => {
    return dispatch => {
        dispatch(requestCreateCustomer(formDataToObject(data)))

        axios_os.post(OS_API.CUSTOMER_CREATE, data)
        .then(function(response) {
            dispatch(receiveCreateCustomer(response.data))
        })
        .catch(function (error) {
            console.log(error)
        })
        .then(function() {
            //always executed
        })
    }
}

// updaters
const updateCustomer = (data) => {
    return dispatch => {
        dispatch(requestUpdateCustomer(formDataToObject(data)))

        axios_os.post(OS_API.CUSTOMER_UPDATE, data)
        .then(function(response) {
            dispatch(receiveUpdateCustomer(response.data))
        })
        .catch(function (error) {
            console.log(error)
        })
        .then(function() {
            //always executed
        })
    }
}

const updateCustomerPicture = (cuID, picture) => {
    return dispatch => {
        dispatch(requestSaveCameraAppSnap())

        let fd = new FormData()
        fd.append('picture', picture)
        fd.append('cuID', cuID)

        axios_os.post(OS_API.CUSTOMER_PICTURE_UPDATE, fd)
        .then(function(response) {
            dispatch(receiveSaveCameraAppSnap(response.data))
        })
        .catch(function (error) {
            console.log(error)
        })
        .then(function() {
            //always executed
        })
    }
}


export default {
    createCustomer,
    updateCustomer,
    updateCustomerPicture,
    fetchCustomers,
    setSearchTimeout,
    clearSearchTimeout,
    setCreateCustomerStatus,
    setUpdateCustomerStatus,
    setDisplayCustomerID,
    clearDisplayCustomerID,
    setSearchCustomerID,
    clearSearchCustomerID,
    setSearchValue,
    clearSearchValue,
    setSelectedCustomerID,
    clearSelectedCustomerID,
    setRedirectNextComponent,
    clearRedirectNextComponent,
    setCameraAppSnap,
    clearCameraAppSnap
}
