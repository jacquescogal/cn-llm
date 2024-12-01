import React from 'react'
import Modal from './common/modal/Modal'
import ReviewForm from './common/forms/ReviewForm'

type Props = {}

const TestPage = (props: Props) => {
  return (
    <div>
        <Modal modalId='what' reactNode={<div className='bg-red-100 h-24 w-48 cursor-pointer'>Review Form</div>} form={<ReviewForm/>}/>
    </div>
  )
}

export default TestPage