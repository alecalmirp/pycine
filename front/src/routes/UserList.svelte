<script>
	let promise;
	async function getUsuarios() {
    // faz um request GET para endpoint /filmes
		const res = await fetch(`http://localhost:8000/user`);
		const text = await res.json();
		if (res.ok) { return text; } 
    else { throw new Error(text);}
	}
	function handleClick() {
		promise = getUsuarios();
	}
</script>

<button on:click={handleClick}> Get usuarios </button>

{#await promise}
	<p>...waiting</p>
{:then usuarios}
	{#if promise != null}
	<h1>Lista de usuarios -</h1>
    <table>
        <tr>
            <th>Id</th>
            <th>Email</th>
        </tr>
    {#each usuarios as usuario}
        <tr>
            <td>{usuario.id}</td>
            <td>{usuario.email}</td>
        </tr>
	{/each}
    </table>
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

