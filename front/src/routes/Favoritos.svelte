<script>
    let promise;
    export let useremail;
    async function getUserFavorites() {
        const res = await fetch(`http://localhost:8000/favorite?email=${useremail}`);
        if (res.status == 200) {
            const text = await res.json();
            return text;
        }
    }

    async function getUserId() {
        debugger;
        const res = await fetch(`http://localhost:8000/user/getUserByEmail?email=${useremail}`);
        if (res.status == 200) {
            const text = await res.json();
            return text;
        }
        
    }

	async function getFavoritos() {
        const text = await getUserFavorites();
        let moviesQueryString = `http://localhost:8000/filmes/getMoviesById?`;
        let i = 0;
        text.forEach(function(element, idx, array) {
            if (idx == 0) {
                moviesQueryString += `ids=${element.idMovie}`;
            }
            else {
                moviesQueryString += `&ids=${element.idMovie}`;
            }
        });
        const res2 = await fetch(moviesQueryString);
        if (res2.status == 200) {
            const text2 = await res2.json();

            return text2;
        }
        else
            alert("Erro desconhecido.");
	}

    async function removerFavoritos(event) {
        debugger;
        const button = event.currentTarget.value;
        let text = await getUserId();
        let data = {
            "idMovie": button,
            "idUser": text.id
        }

        await fetch(`http://localhost:8000/favorite`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        document.querySelector(`#favorito${button}`).style.display = "none"
    }

    function setEvent() {
        promise = getFavoritos();
    }
</script>

<button id="getFilmes" on:click={setEvent}> Get favoritos </button>

{#await promise}
	<p>...waiting</p>
{:then favoritos}
	{#if promise != null}
	<h1>Lista de favoritos -</h1>
	<ul>
    {#each favoritos as favorito}
		<li id="favorito{favorito.id}">
			<img src={favorito.imagem} alt="Imagem do poster do filme">
			<p>{favorito.nome} | <button value="{favorito.id}" on:click={removerFavoritos}>- Desfavoritar</button></p>
		</li>
	{/each}
	</ul>
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}