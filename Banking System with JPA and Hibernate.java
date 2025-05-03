import javax.persistence.*;
import java.util.*;
import java.math.BigDecimal;

@Entity
@Table(name = "accounts")
class Account {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String accountNumber;
    private BigDecimal balance;
    
    @OneToMany(mappedBy = "account", cascade = CascadeType.ALL)
    private List<Transaction> transactions = new ArrayList<>();
    
    // Constructors, getters, setters
    public void addTransaction(Transaction transaction) {
        transactions.add(transaction);
        transaction.setAccount(this);
    }
}

@Entity
@Table(name = "transactions")
class Transaction {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private BigDecimal amount;
    private Date timestamp;
    
    @ManyToOne
    @JoinColumn(name = "account_id")
    private Account account;
    
    // Constructors, getters, setters
}

public class BankingSystem {
    private EntityManagerFactory emf = Persistence.createEntityManagerFactory("banking-system");

    public void transfer(Long fromAccountId, Long toAccountId, BigDecimal amount) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        
        try {
            tx.begin();
            
            Account from = em.find(Account.class, fromAccountId);
            Account to = em.find(Account.class, toAccountId);
            
            if (from.getBalance().compareTo(amount) < 0) {
                throw new RuntimeException("Insufficient funds");
            }
            
            from.setBalance(from.getBalance().subtract(amount));
            to.setBalance(to.getBalance().add(amount));
            
            Transaction debit = new Transaction(amount.negate(), new Date());
            Transaction credit = new Transaction(amount, new Date());
            
            from.addTransaction(debit);
            to.addTransaction(credit);
            
            em.persist(debit);
            em.persist(credit);
            
            tx.commit();
        } catch (Exception e) {
            if (tx.isActive()) tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }

    public static void main(String[] args) {
        BankingSystem bank = new BankingSystem();
        bank.transfer(1L, 2L, new BigDecimal("100.00"));
    }
}