<template>
  <div>
    <h2>Top 10 Movies</h2>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Title</th>
          <th>Release Year</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(movie, index) in top10Movies" :key="movie.movieId">
          <td>{{ index + 1 }}</td>
          <td>{{ movie.title }}</td>
          <td>{{ movie.year }}</td>
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
      top10Movies: [],
    };
  },
  async mounted() {
    const moviesResponse = await axios.get('/data/movie.csv');
    const moviesData = Papa.parse(moviesResponse.data, { header: true }).data;

    this.calculateTop10Movies(moviesData);
  },
  methods: {
    calculateTop10Movies(moviesData) {
      this.top10Movies = moviesData
        .sort((a, b) => b.rating - a.rating)
        .slice(0, 10)
        .map((movie) => ({
          title: movie.title,
          year: movie.year,
        }));
    },
  },
};
</script>

<style>
/* Add your component-specific styles here */
</style>
