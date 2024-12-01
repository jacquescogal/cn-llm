import { CardType, ReviewDTO, ReviewType } from '../../../types/dto';

const ReviewForm = (props:ReviewDTO) => {
    console.log(props)
  return (
    <div>
        {props.card_type === CardType.Meaning &&
        <>
        {
            props.review_type === ReviewType.OpenEnded && "Meaning Open Ended"
        }
        {
            props.review_type === ReviewType.MCQ && "Meaning MCQ"
        }
        {
            props.review_type === ReviewType.OCR && "Meaning OCR"
        }
        {
            props.review_type === ReviewType.DRAG_AND_DROP && "Meaning Drag and Drop"
        }
        </>
        }
    </div>
  )
}

export default ReviewForm