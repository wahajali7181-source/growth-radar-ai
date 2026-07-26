import os


def build_react_template(data):

    project = f"""
import './App.css'

function App() {{

return (

<div>

<section className="hero">

<h1>{data['hero']['title']}</h1>

<p>{data['hero']['description']}</p>

<button>

{data['hero']['button']}

</button>

</section>

</div>

)

}}

export default App
"""

    return project