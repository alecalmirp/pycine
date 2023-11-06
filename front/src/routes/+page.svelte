<script>
	let menu = 1;
	let useremail = "alec"
	import Movie from "./Movie.svelte";
	import Artista from "./Artist.svelte";
	import Nav from "./Nav.svelte";
	import User from "./User.svelte";
	import UserList from "./UserList.svelte";
	import Favoritos from "./Favoritos.svelte";
</script>

<Nav bind:menu/>

<div class="card">
	{#if menu === 1}
		<Movie bind:useremail/>
	{:else if menu === 2}
		<Favoritos bind:useremail/>
	{:else if menu === 3}
		<Artista/>
	{:else if menu === 4}
		<User/>
	{:else if menu === 5}
		<UserList/>
	{:else}
		OPTION 5
	{/if}
</div>