import './Search.css';

export default function Search(props) {
  const search_onchange = (event) => {
    props.setSearch(event.target.value);
  }

  return (
    <div className='search_field'>
      <input
        type='text'
        placeholder='Search Cruddur'
        value={props.search}
        onChange={search_onchange}
      />
    </div>
  );
}