import { WordDTO } from '../../types/dto';
type HTMLElementModal = HTMLElement & {
  showModal: () => void;
  close: () => void;
};
const WordPreviewCard =(props:{modalId:string, word:WordDTO})=> {
  return (
    <>
      <button
      className=' w-0 h-0'
        onClick={() =>
          (document.getElementById(
            props.modalId
          ) as HTMLElementModal)!.showModal()
        }
      >
      </button>
      <dialog id={props.modalId} className="modal">
        <div className="modal-box w-fit max-w-fit">
          <div className="bg-base-100 text-base-content rounded-lg h-[35rem] w-[50rem] flex flex-row">
            <form method="dialog">
              {/* if there is a button in form, it will close the modal */}
              <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={e=>{e.preventDefault()}}>
                ✕
              </button>
            </form>
            <div className="bg-black w-7/12 flex-0 h-full"></div>

            <div className="bg-black w-full flex-1 h-full flex flex-col">
              <div className="bg-red-100 w-full h-full"></div>
              <div className="bg-blue-100 w-full h-full"></div>
            </div>
          </div>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </>
  );
};

export default WordPreviewCard;
