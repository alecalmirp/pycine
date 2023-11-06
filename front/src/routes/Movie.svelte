<script>
	import { browser } from '$app/environment';
	export let useremail;

	let promise;
	async function getFilmes() {
	    // faz um request GET para endpoint /filmes
	    const res = await fetch(`http://localhost:8000/filmes/getMovieInfo`);
	    const text = await res.json();
	    if (res.ok) 
	        return text;
	    else 
	        throw new Error(text);
	}

	async function favoritarFilme(event) {
		debugger;
		const buttonValue = event.currentTarget.value;
		let res1 = await fetch(`http://localhost:8000/user/getUserByEmail?email=${useremail}`);
		if (res1.status == 200) {
			let usuario = await res1.json();
			const data = {
			"idMovie": parseInt(buttonValue),
			"idUser": parseInt(usuario.id)
			}
			const res2 = await fetch(`http://localhost:8000/favorite`, {
			method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
			body: JSON.stringify(data)
			})
			if (res2.status == 409) {
				alert("Esse filme já foi favoritado!");
			}
			else
				alert("Filme adicionado aos favoritos!");
		}
		else
			alert("Email inválido!");
	}

	function setEvent() {
		promise = getFilmes();
	}
</script>

<button on:click={setEvent}> Get filmes </button>

{#await promise}
	<p>...waiting</p>
{:then filmes}
	{#if promise != null}
	<h1>Lista de filmes -</h1>
	<ul>
    {#each filmes as filme}
		<li>
			<img src={filme.imagem} alt="Imagem do poster do filme">
			<p>{filme.nome} | <button value="{filme.id}" on:click={favoritarFilme}>+ Favoritar</button></p>
		</li>
	{/each}
	</ul>
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

