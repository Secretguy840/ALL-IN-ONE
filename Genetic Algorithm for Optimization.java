import java.util.*;
import java.util.stream.*;

public class GeneticAlgorithm {
    private static final int POPULATION_SIZE = 100;
    private static final double MUTATION_RATE = 0.01;
    private static final int TOURNAMENT_SIZE = 5;
    private static final int NUM_GENERATIONS = 100;

    static class Individual {
        int[] genes;
        double fitness;

        Individual(int length) {
            this.genes = new int[length];
            Random rand = new Random();
            for (int i = 0; i < genes.length; i++) {
                genes[i] = rand.nextInt(2); // Binary genes
            }
            calculateFitness();
        }

        void calculateFitness() {
            // Maximize number of 1s (simple example)
            this.fitness = Arrays.stream(genes).sum();
        }

        Individual crossover(Individual other) {
            Individual child = new Individual(genes.length);
            int crossoverPoint = new Random().nextInt(genes.length);
            for (int i = 0; i < genes.length; i++) {
                child.genes[i] = i < crossoverPoint ? this.genes[i] : other.genes[i];
            }
            return child;
        }

        void mutate() {
            Random rand = new Random();
            for (int i = 0; i < genes.length; i++) {
                if (rand.nextDouble() < MUTATION_RATE) {
                    genes[i] = 1 - genes[i]; // Flip bit
                }
            }
        }
    }

    public static void main(String[] args) {
        List<Individual> population = IntStream.range(0, POPULATION_SIZE)
            .mapToObj(i -> new Individual(20))
            .collect(Collectors.toList());

        for (int gen = 0; gen < NUM_GENERATIONS; gen++) {
            // Selection
            List<Individual> newPopulation = new ArrayList<>();
            for (int i = 0; i < POPULATION_SIZE; i++) {
                Individual parent1 = tournamentSelection(population);
                Individual parent2 = tournamentSelection(population);
                Individual child = parent1.crossover(parent2);
                child.mutate();
                child.calculateFitness();
                newPopulation.add(child);
            }
            population = newPopulation;

            // Statistics
            double avgFitness = population.stream()
                .mapToDouble(ind -> ind.fitness)
                .average()
                .orElse(0);
            System.out.printf("Gen %d: Avg fitness %.2f%n", gen, avgFitness);
        }
    }

    static Individual tournamentSelection(List<Individual> population) {
        return new Random().ints(TOURNAMENT_SIZE, 0, population.size())
            .mapToObj(population::get)
            .max(Comparator.comparingDouble(ind -> ind.fitness))
            .orElseThrow();
    }
}