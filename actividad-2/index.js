#!/usr/bin/node

async function fetchPokemon(pokemon) {
  if (pokemon === undefined) {
    throw new Error('Pokemon name must be a string')
  }
  if (!new RegExp('^[a-z]+$').test(pokemon)) {
    throw new Error('The pokemon name can only contain lowercase letters')
  }
  const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`)
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Unknown pokemon')
    }
    throw new Error(`${response.status} (${response.statusText})`)
  }
  return await response.json()
}

async function main () {
  try {
    const pokemonData = await fetchPokemon(process.argv[2])
    console.log(`Name: ${pokemonData.name}`)
    console.log(`Types: ${pokemonData.types.map(v => v.type.name).join(', ')}`)
  } catch (error) {
    console.error(error.message)
  }
}

main()
