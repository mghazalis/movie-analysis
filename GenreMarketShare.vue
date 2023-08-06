<template>
  <div>
    <h2>Genre Market Share</h2>
    <table>
      <thead>
        <tr>
          <th>Genre</th>
          <th>Market Share (%)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(genreData, genre) in genreMarketShare" :key="genre">
          <td>{{ genre }}</td>
          <td>{{ genreData.marketShare.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import Papa from 'papaparse';

export default {
  data() {
    return {
      genreMarketShare: {},
    };
  },
  async mounted() {
    const moviesResponse = await axios.get('/data/movie.csv');
    const moviesData = Papa.parse(moviesResponse.data, { header: true }).data;

    this.calculateGenreMarketShare(moviesData);
  },
  methods: {
    calculateGenreMarketShare(moviesData) {
      const genreCounts = {};
      const totalMovies = moviesData.length;

      moviesData.forEach((movie) => {
        if (movie.genres) {
          const genres = movie.genres.split('|');
          genres.forEach((genre) => {
            genreCounts[genre] = genreCounts[genre] ? genreCounts[genre] + 1 : 1;
          });
        }
      });

      this.genreMarketShare = Object.entries(genreCounts).reduce((result, [genre, count]) => {
        const marketShare = (count / totalMovies) * 100;
        result[genre] = { count, marketShare };
        return result;
      }, {});
    },
  },
};
</script>

<style>
/* Add your component-specific styles here */
</style>
