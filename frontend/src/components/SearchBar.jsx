function SearchBar({

    search,

    setSearch,

    status,

    setStatus

}) {

    return (

        <div className="search-row">

            <input

                placeholder="Search invoice/vendor..."

                value={search}

                onChange={(e)=>

                    setSearch(e.target.value)

                }

            />

            <select

                value={status}

                onChange={(e)=>

                    setStatus(e.target.value)

                }

            >

                <option>

                    ALL

                </option>

                <option>

                    VALID

                </option>

                <option>

                    INVALID

                </option>

            </select>

        </div>

    );

}

export default SearchBar;