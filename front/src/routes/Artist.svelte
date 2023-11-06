<script>
	let artista;
	async function getArtista() {
    // faz um request GET para endpoint /atores
        const id = document.getElementById("artista");
		const res = await fetch("http://localhost:8000/atores/" + id.value);
		const text = await res.json();
		if (res.ok) { return text; } 
    else { throw new Error(text);}
	}
	function handleClickArtista() {
		artista = getArtista();
	}
</script>

<input type="number" id="artista">
<button on:click={handleClickArtista}> Get Artista </button>

{#await artista}
	<p>...waiting</p>
{:then artista}
	{#if artista != null}
	<h1>Artista -</h1>
		<p>{artista.biography}</p>
        <img src="https://image.tmdb.org/t/p/w185{artista.profile_path}" alt="Imagem do Artista {artista.name}">
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

