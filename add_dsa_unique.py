import json
import random

with open('questions.json', 'r') as f:
    questions = json.load(f)

questions = [q for q in questions if q.get('topic') != 'DSA']

easy_scenarios = [
    ("You're given an array where every element appears twice except one unique element. Find the unique element without extra space - explain the bit manipulation approach.", "Use XOR: a ^ a = 0, a ^ 0 = a. XOR all elements, result is unique. Time O(n), Space O(1)."),
    ("A delivery truck must visit multiple cities and return to depot. The distances are known - find shortest route. What algorithm solves this traveling salesman scenario?", "For small n, brute force all permutations O(n!). For larger, use nearest neighbor heuristic or dynamic programming with bitmask O(n²*2^n). Consider branch and bound for pruning."),
    ("E-commerce platform needs to sort 1 million products by price. Products change frequently. Which sorting algorithm and why for this real-time scenario?", "Quick sort for average O(n log n). For nearly sorted, insertion sort O(n). Consider hybrid: quicksort large chunks, insertion for small. In-place preferred."),
    ("Text editor needs autocomplete - user types prefix, show matching words from dictionary. What data structure gives O(1) prefix lookup?", "Trie (prefix tree): insert words, traverse by prefix. Search O(m) where m=prefix length. Optimize with pruning and frequency-based suggestions."),
    ("Social media app shows 'people you may know'. Connections as graph, find friends-of-friends excluding already connected. Efficient implementation?", "BFS from current user at depth 2. Use set for O(1) lookup of connected. Skip direct friends. Time O(V+E), Space O(n)."),
    ("Design stack supporting push, pop, and getMin in O(1). Use case: transaction system tracking minimum balance. How to implement?", "Two stacks: main for elements, min stack tracking minimum at each push. On push: also push to min if <= current min. Space O(n), operations O(1)."),
    ("Find longest palindromic substring in string. Real use: DNA sequence analysis finding restriction sites. Which approach works efficiently?", "Expand around center: O(n²) time, O(1) space. For DNA, suffix tree gives O(n). Consider Manacher's O(n) algorithm."),
    ("Merge two sorted arrays into one sorted array without extra space. Scenario: merging sorted logs from multiple servers.", "Start from end of both arrays (largest), place in result from end. Time O(m+n), Space O(1). Standard merge adapted for in-place."),
    ("Find subarray with maximum sum. Scenario: analyzing stock prices to find best buy-sell period. Handle edge case of all negative numbers.", "Kadane's algorithm: track max ending here and max so far. Handle all negatives by returning largest (or 0 if allowed). Time O(n), Space O(1)."),
    ("Remove duplicates from sorted array in-place. Scenario: sensor data cleanup removing duplicate readings. Two-pointer approach explained.", "Two pointers: one for result position, one for traversal. Skip duplicates, copy unique. Time O(n), Space O(1). Return new length."),
    ("Implement queue using two stacks. Scenario: task scheduler with priority. Explain amortized O(1) operations.", "Enqueue stack for push, dequeue stack for pop. Transfer elements when dequeue empty. Amortized O(1) for both operations."),
    ("Find intersection of two linked lists without modifying them. Scenario: two train routes merging - find meeting station.", "Calculate lengths, advance longer list by difference, traverse together. Time O(m+n), Space O(1). Can also use hash set approach."),
    ("Reverse linked list in groups of k. Scenario: chat pagination showing k messages per page. Handle incomplete last group.", "Iterative with prev, curr, next pointers. Track group start for next iteration. Handle remaining < k appropriately."),
    ("Validate parentheses sequence. Scenario: code editor checking balanced brackets. Stack-based solution explained.", "Push opening, pop and match on closing. Stack empty at end means valid. Time O(n), Space O(n) worst case."),
    ("Climbing stairs with variable steps. Scenario: stairs with 1 or 2 steps, but some steps blocked. DP approach with constraints.", "DP[i] = DP[i-1] + DP[i-2] (if not blocked). Optimize to O(1) space. Handle blocked steps by marking invalid."),
    ("Find element appearing more than n/2 times. Scenario: determining majority opinion in group decision. Boyer-Moore explained.", "Maintain candidate and count. Increment on match, decrement otherwise. Verify candidate at end. Time O(n), Space O(1)."),
    ("Move zeros to end preserving relative order. Scenario: processing event log with null events at end. Two-pointer solution.", "Two pointers: slow for result, fast for traversal. Swap non-zero to slow. Time O(n), Space O(1)."),
    ("Find peak in mountain array. Scenario: terrain analysis finding highest point. Binary search optimization.", "Binary search: compare mid with mid+1. If increasing, search right. Otherwise search left. Time O(log n), Space O(1)."),
    ("Find common elements between two arrays without duplicates. Scenario: finding products in both warehouses. Set vs two-pointer.", "HashSet: O(m+n) time. Two-pointer after sorting: O(n log n + m log m). Choose based on input size."),
    ("Check if two strings are anagrams. Scenario: word game checking letter rearrangement. Frequency array approach.", "Count frequency with array[26]. Compare counts. Time O(n), Space O(1). Alternative: sort strings O(n log n)."),
    ("Find missing number in array 1 to n. Scenario: finding absent employee ID from sequence. XOR or formula approach.", "XOR all numbers 1 to n and all array elements. Result is missing. Or use sum formula: n*(n+1)/2 - sum."),
    ("Reverse words in sentence without reversing characters. Scenario: processing message format. In-place approach.", "Reverse entire string, then reverse each word. Or split, reverse, join. Time O(n), Space O(1) or O(n)."),
    ("Check if string contains duplicate characters. Scenario: license key validation. Set vs bit manipulation.", "Use boolean array[26] or bit vector for 26 letters. If char already seen, duplicate exists. O(n) time, O(1) space."),
    ("Find pair in array summing to target. Scenario: transaction pair finding in logs. Hash map vs two-pointer.", "Hash map: O(n) time, O(n) space. Two-pointer: sort first O(n log n), then search O(n). Choose based on space."),
    ("Count occurrences of sorted array element. Scenario: finding frequency of search term in logs. Binary search for boundaries.", "Binary search for first and last occurrence. Count = last - first + 1. Time O(log n) for each boundary."),
    ("Find square root using binary search. Scenario: calculating dimensions from area. Precision handling.", "Binary search between 0 and n. Check mid*mid <= n < (mid+1)*(mid+1). Handle precision requirements."),
    ("Check if number is power of two. Scenario: checking memory block allocation validity. Bit manipulation.", "n > 0 and (n & (n-1)) == 0. Or count set bits == 1. Time O(1), Space O(1)."),
    ("Find GCD of two numbers. Scenario: simplifying fractions in calculation. Euclidean algorithm.", "gcd(a, b) = gcd(b, a%b). Continue until b=0. Time O(log min(a,b)). Iterative or recursive."),
    ("Convert decimal to binary. Scenario: network IP address conversion. String building approach.", "Divide by 2, collect remainders. Build string from end. Handle 0 case. Time O(log n)."),
    ("Find duplicate in array 1 to n. Scenario: finding repeated employee ID. Floyd's tortoise and hare.", "Floyd's cycle detection: slow and fast pointers. When they meet, reset slow and move both. Find intersection."),
    ("Search insert position in sorted array. Scenario: finding insertion point for new sorted element. Binary search.", "Binary search with condition for target <= nums[mid]. Return mid position. Handle edge cases."),
    ("Implement atoi string to integer. Scenario: parsing user input number. Handle overflow and invalid input.", "Handle spaces, signs, overflow. Stop at non-digit. Check INT_MAX/INT_MIN bounds. Time O(n)."),
    ("Find maximum consecutive ones. Scenario: analyzing network uptime. Sliding window with zero count.", "Sliding window tracking zeros. Expand right, shrink left when zeros > k. Track max length. Time O(n)."),
    ("Rotate array by k positions. Scenario: circular buffer for streaming data. Reversal algorithm explained.", "Reverse entire array, reverse first k, reverse rest. Or direct cyclic replacement. Time O(n), Space O(1)."),
    ("Check if linked list has cycle. Scenario: detecting circular dependency in organization. Floyd's algorithm.", "Slow and fast pointers. If they meet, cycle exists. Find start by resetting one pointer."),
    ("Find first unique character in string. Scenario: finding first non-repeated request ID. Hash map frequency.", "Build frequency map. Second pass find first with count 1. Time O(n), Space O(1) for 26 chars."),
    ("Merge sorted linked lists. Scenario: combining sorted transaction logs. Dummy node approach.", "Use dummy head. Compare nodes, attach smaller. Handle remaining nodes. Time O(n+m), Space O(1)."),
    ("Find equilibrium index in array. Scenario: finding balance point in weight distribution. Prefix sum approach.", "Calculate total sum. Iterate with running sum. Check if left sum equals right sum at each index."),
    ("Check if binary tree is balanced. Scenario: validating organizational hierarchy depth. Recursive height check.", "Recursively get height. Return -1 if unbalanced. Compare left and right heights. Time O(n)."),
    ("Find minimum in rotated sorted array. Scenario: finding lowest element after rotation. Modified binary search.", "Binary search: compare mid with end. If mid < end, search left. Else search right. Time O(log n)."),
    ("Count bits in number. Scenario: calculating information entropy. Brian Kernighan's algorithm.", "n & (n-1) clears lowest set bit. Count iterations. Time O(set bits), Space O(1)."),
    ("Add two numbers as linked lists. Scenario: adding two account balances digit by digit. Handle carry.", "Traverse both lists, add digits with carry. Create new node for each sum. Handle different lengths."),
]

medium_scenarios = [
    ("Design LRU cache for browser. Scenario: caching visited web pages. What data structures give O(1) operations for both get and put?", "HashMap for O(1) lookup + Doubly Linked List for O(1) eviction order. Head=most recent, Tail=least recent. Move to head on access. Evict from tail on capacity."),
    ("Serialize and reconstruct binary tree. Scenario: storing organizational chart in database. Efficient serialization format?", "Pre-order traversal with null markers. For compactness, level-order with indices. Choose between size and reconstruction speed."),
    ("Find median from infinite data stream. Scenario: real-time analytics showing median response time. Two heaps approach.", "Max heap for lower half, min heap for upper half. Balance sizes on each insert. Median from heap tops. O(log n) insert, O(1) query."),
    ("Word break into dictionary words. Scenario: autocomplete forming sentences. DP solution with trie optimization.", "DP[i] = true if DP[j] && s[j:i] in dict. Optimize with trie for early termination. Handle pathological large dictionary cases."),
    ("Longest increasing subsequence. Scenario: stock profit where you can buy once before selling. DP vs patience sorting.", "DP O(n²) or patience sorting O(n log n). For stock with one transaction, simpler O(n) greedy exists."),
    ("Trapping rainwater between buildings. Scenario: water collection in terrain. Two-pointer vs stack approach.", "Two-pointer: move from ends, track max heights. Stack: push when current > stack top. Calculate water. Time O(n), Space O(1) or O(n)."),
    ("Calculate edit distance between strings. Scenario: spell checker suggesting corrections. Levenshtein with optimizations.", "DP table: min(insert, delete, replace). Base cases for empty strings. Optimize to O(min(m,n)) space. Consider early termination."),
    ("Container with most water between vertical lines. Scenario: maximizing cargo in container sections. Two-pointer proof.", "Move pointers inward, shrink shorter line (limiting factor). Prove no better solution between. Time O(n), Space O(1)."),
    ("Jump game determining reachability. Scenario: game character jumping on platforms. Greedy vs DP.", "Greedy: track farthest reachable, fail if current > farthest. DP: dp[i] reachable from start. Time O(n), Space O(1) greedy."),
    ("Coin change with minimum coins. Scenario: making change minimizing coin count. DP with early termination.", "DP[i] = min(DP[i-coin] + 1). Bottom-up 1D array. Handle impossible case. Add early termination for large amounts."),
    ("Subarray sum equals k with multiple solutions. Scenario: finding time ranges in logs summing to duration. Hash map optimization.", "Prefix sum with hash map for O(n). Count prefix sum occurrences. Handle negative numbers by storing all."),
    ("Count islands in grid. Scenario: connected components in map. BFS/DFS vs Union-Find.", "DFS: traverse and mark visited, count components. BFS with queue. Union-Find for dynamic additions. Time O(m*n)."),
    ("Clone linked list with random pointer. Scenario: copying org chart with reporting lines. Hash map vs O(1) space.", "Hash map: original->copy mapping O(n) space. Optimized: interweave copies in list, then separate. O(1) space but modifies list."),
    ("Find first missing positive integer. Scenario: finding smallest available ID from pool. In-place modification.", "Place each positive at index n-1. Scan for first positive. Handle edge case of all positives. Time O(n), Space O(1)."),
    ("Maximum product subarray. Scenario: most profitable trade sequence with sign changes. Handle zeros and negatives.", "Track max and min ending at each position. New max = max(curr, max*curr, min*curr). Reset on zero. Time O(n), Space O(1)."),
    ("Rotate matrix 90 degrees in-place. Scenario: rotating game board. Layer-by-layer rotation.", "Process layers from outside in. Rotate 4 elements at a time in cycle. Time O(n²), Space O(1)."),
    ("Longest substring without repeating chars. Scenario: unique character detection in stream. Sliding window with hash.", "Expand right, shrink left on duplicate. Use hash map for positions. Track max. Time O(n), Space O(min(charset, n))."),
    ("Merge overlapping intervals. Scenario: meeting room scheduling conflicts. Sorting approach.", "Sort by start time. Merge while next.start <= current.end. Handle contained, touching, disjoint. Time O(n log n)."),
    ("Search in rotated sorted array. Scenario: finding element after rotation. Modified binary search.", "Find pivot (minimum). Decide which half to search. Compare with boundaries. Handle duplicates with extra check. O(log n) avg."),
    ("Design data structure for union-find. Scenario: detecting cycles in graph for network connections.", "Path compression and union by rank. Find with compression, union by rank. Detect cycle during edge addition."),
    ("Implement topological sort. Scenario: build system dependency resolution. Kahn's algorithm vs DFS.", "Kahn: BFS with in-degree counting. DFS: post-order reversal. Both O(V+E). Handle cycle detection."),
    ("Find diameter of binary tree. Scenario: calculating longest path in network. Two DFS approach.", "For each node, get max depth of children. Diameter = max(left + right + 1). Track global max during traversal. O(n)."),
    ("Validate binary search tree. Scenario: checking if organization levels are valid. In-order traversal.", "In-order traversal should be sorted. Track previous node to compare. Time O(n), Space O(h) for recursion."),
    ("Find all permutations of string. Scenario: generating all possible codes. Backtracking with swap.", "Swap each character with subsequent, recurse, backtrack. Use visited set to avoid duplicates. Time O(n! * n)."),
    ("Implement trie with insert and search. Scenario: autocomplete system with prefix matching.", "Node with children map and end marker. Insert: create nodes for each char. Search: traverse path. Space: O(alphabet * n)."),
    ("Binary tree level order traversal. Scenario: processing organizational hierarchy level by level. BFS with queue.", "Use queue for BFS. Process each level, collect nodes. Can store level markers or use size-based iteration. Time O(n)."),
    ("Find all anagrams together. Scenario: grouping similar transaction descriptions. Sort and hash approach.", "Sort each string, use as key in hash map. Group anagrams together. Time O(n * k log k)."),
    ("Implement quick sort with partitioning. Scenario: sorting user data by timestamp. Hoare vs Lomuto partition.", "Lomuto: pivot at end, partition around it. Hoare: two pointers from ends. Handle duplicates. Time O(n log n) avg."),
    ("Find subset sum equals target. Scenario: resource allocation problem. DP with boolean array.", "DP[i][j] = true if subset with sum j exists using first i elements. Space optimize to 1D. Time O(n * target)."),
    ("Maximum sum of non-adjacent elements. Scenario: robbing houses without triggering alarm. DP with two states.", "DP[i] = max(DP[i-1], DP[i-2] + arr[i]). Optimize to O(1) space. Handle single element edge case."),
    ("Decode ways for digit sequence. Scenario: decoding encrypted message. DP with validation.", "DP[i] = ways to decode s[i:]. Check single (1-9) and double (10-26). Handle 0 cases. Time O(n), Space O(n)."),
    ("Find number of ways to reach nth stair. Scenario: climbing stairs with 1 or 2 steps. DP recurrence.", "DP[n] = DP[n-1] + DP[n-2]. Can optimize to O(1) space. Handle large results with modulo."),
    ("Longest common substring. Scenario: DNA sequence matching. DP table approach.", "DP[i][j] = length of LCS ending at i,j. Track max. Time O(m*n), Space O(m*n) or optimize."),
    ("Find all paths in matrix from start to end. Scenario: robot navigation in grid. DFS with backtracking.", "Explore all paths, mark visited, backtrack. Handle obstacles. Time exponential, space O(path length)."),
    ("Implement minimum heap. Scenario: priority queue for task scheduling. Heapify and push/pop.", "Array representation. Push: append, bubble up. Pop: swap with last, bubble down. Heapify: bubble down from last parent. O(log n)."),
    ("Count ways to form string with adjacent pairs. Scenario: building valid string sequences. DP with adjacent checks.", "DP[i] = sum of DP[j] where j->i is valid. Handle boundary conditions. Time O(n * k)."),
    ("Find minimum path sum in triangle. Scenario: optimal path through hierarchy. Bottom-up DP.", "DP from bottom: dp[i][j] = min(dp[i+1][j], dp[i+1][j+1]) + val. Optimize to 1D. Time O(n²)."),
    ("Stock buy-sell for maximum profit with cooldown. Scenario: trading with rest period between trades. State machine DP.", "States: hold, rest, sold. Transition between states. Track max profit in each state. Time O(n), Space O(1)."),
    ("Find minimum vertices to reach all nodes. Scenario: minimum starting points for network coverage. BFS from all sources.", "Add all source nodes to queue initially. BFS to get distances. Nodes with min distance are answer. Time O(V+E)."),
]

hard_scenarios = [
    ("Design system for shortest path in dynamic graph with frequently changing edge weights. Scenario: real-time traffic navigation with live updates. What data structures handle this efficiently?", "Dynamic shortest path: incremental updates vs full recomputation. Use Johnson's reweighting. Consider ALT (A* with Landmarks) for speedup. Handle partial updates efficiently."),
    ("Implement best-fit memory allocator. Scenario: embedded system with limited memory. Handle fragmentation and allocation.", "Segregated free lists by size class. Search within class for best fit. Coalesce on free with boundary tags. Calculate metadata overhead."),
    ("Design segment tree for range minimum queries with updates. Scenario: real-time stock price monitoring with range queries.", "Build O(n), query O(log n), update O(log n). Lazy propagation for range updates. Space O(4n). Can also use Fenwick tree for simpler cases."),
    ("Find median of two sorted arrays. Scenario: merging data streams from different sources. Optimized binary search.", "Binary search on smaller array, calculate partition. Handle boundary edge cases. Time O(log(min(m,n))), Space O(1)."),
    ("Word ladder transformation. Scenario: building word chain for word game. BFS vs bidirectional BFS.", "BFS from both ends, meet in middle. Optimize neighbor generation with wildcard patterns. Use hash set for O(1) lookup. Avoid cycles."),
    ("Trapping water in 2D terrain. Scenario: water accumulation in geographical map. Priority queue flood fill.", "Start from boundaries with min-heap. Track visited. Calculate water trapped based on boundary max. Time O(m*n*log(m*n)), Space O(m*n)."),
    ("Find kth smallest in two sorted arrays. Scenario: finding median from merged data sources. Binary search proof.", "Binary search k in smaller array, calculate remaining. Handle edge cases. Time O(log(min(m,n))). Verify with examples."),
    ("Maximum flow in network. Scenario: network routing with bandwidth constraints. Ford-Fulkerson vs Edmonds-Karp vs Dinic.", "Ford-Fulkerson: O(E*maxflow). Edmonds-Karp: BFS augmenting O(VE²). Dinic: level graph + blocking flow O(V²E). Choose based on network."),
    ("Longest common subsequence with space optimization. Scenario: DNA sequence alignment. DP with rolling array.", "DP[i][j] = LCS length. Optimize to O(min(m,n)) space with two rows. Hirschberg for O(1) space with path reconstruction."),
    ("Traveling salesman for delivery optimization. Scenario: delivery truck visiting multiple locations. Exact vs approximation.", "Exact: O(n!) brute force, DP O(n²*2^n). Approximation: nearest neighbor, Christofides (1.5x). Branch and bound for smaller instances."),
    ("Design real-time top-k streaming system. Scenario: trending topics monitoring. Data structure choices.", "Min-heap of size k for top-k. Compare incoming with heap top. For approximate large-k, use count-min sketch."),
    ("Solve Sudoku with constraint propagation. Scenario: puzzle solving algorithm with backtracking optimization.", "Bitmasks for candidates. Apply constraint propagation (naked/hidden singles). Choose most constrained cell. Pruning reduces search dramatically."),
    ("Implement LFU cache with O(1). Scenario: web cache with frequency-based eviction. Two-level data structure.", "Hash map for key->node + freq list with doubly linked lists. Increment freq on access, move between lists. Evict from freq=1. Time O(1)."),
    ("Serialize and compress trie. Scenario: storing dictionary efficiently. Encoding strategies.", "DFS pre-order with markers. Compress repeated paths. Store frequency for autocomplete. Consider radix trie for compression."),
    ("Find strongly connected components. Scenario: analyzing build system dependencies. Kosaraju vs Tarjan.", "Kosaraju: DFS finish order, reverse graph, DFS on reversed. Tarjan: single DFS with stack and low-link. Both O(V+E). Tarjan in one pass."),
    ("Maximum subsequence with k distinct numbers. Scenario: selecting k distinct stocks for portfolio. DP optimization.", "DP[i][k] = max sum ending at i with k elements. Optimize from O(n*k*n) to O(n*k) with sliding window. Track best at each position."),
    ("Design bloom filter for spell checker. Scenario: checking word existence in dictionary. False positive analysis.", "Multiple hash functions, bitmap array. Calculate optimal: m = -n*ln(p)/(ln(2)²), k = (m/n)*ln(2). Trade space for false positives."),
    ("Shortest path with constraints. Scenario: routing with edge weight limits (fuel). State expansion approach.", "Expand state to include constraint (remaining fuel). Modified Dijkstra with state. Handle multi-dimensional constraints."),
    ("Implement Aho-Corasick for multi-pattern matching. Scenario: keyword detection in text stream. Failure links.", "Build trie, compute failure links via BFS. Process text: follow goto or failure. Collect matches via output links. Time O(text + patterns + matches)."),
    ("Matrix chain multiplication optimization. Scenario: optimal computation order for matrices. DP with chain tracking.", "DP[i][j] = min cost. Recurrence: DP[i][j] = min(DP[i][k] + DP[k+1][j] + dims[i]*dims[k+1]*dims[j+1]). Build solution table. O(n³), O(n²)."),
    ("Design system for concurrent task scheduling with dependencies. Scenario: build system with parallel tasks. Topological + priority queue.", " Kahn's algorithm with priority queue for same-level tasks. Handle dynamic additions. Minimize total execution time."),
    ("Find minimum cost to connect n points. Scenario: network setup cost minimization. Prim vs Kruskal vs Boruvka.", "Prim: O(E log V) with heap. Kruskal: O(E log V) with union-find. Boruvka: O(E log V) with multiple components. Choose based on edge density."),
    ("Implement custom string matching with wildcards. Scenario: file pattern matching. Dynamic programming approach.", "Build DP table matching pattern chars with string. Handle * (any chars) and ? (single char). Time O(m*n)."),
    ("Design rate limiter with sliding window. Scenario: API rate limiting per user. Data structures for efficient tracking.", "Use deque or circular buffer for timestamps. Remove expired entries on each request. Check count within window. O(1) operations."),
    ("Find all palindromic partitions. Scenario: breaking string into palindromes. Backtracking with pruning.", "Generate all substrings, check palindrome. Backtrack to build partitions. Prune by checking remaining can't form palindrome. Time exponential."),
    ("Implement thread pool with task scheduling. Scenario: parallel task execution. Queue and worker threads.", "Use blocking queue for tasks. Worker threads consume from queue. Implement shutdown and timeout handling. Handle thread creation overhead."),
    ("Design distributed lock system. Scenario: distributed resource access. Zookeeper or Redis-based implementation.", "Use distributed consensus. Implement lock acquisition with TTL. Handle client failure with automatic expiration. Prevent deadlocks."),
    ("Find minimum time to finish all tasks with dependencies. Scenario: project scheduling with prerequisites. Critical path method.", "Topological sort to get order. Calculate earliest start times. Find critical path (longest sequence). Total time = longest path."),
    ("Implement consistent hashing for distributed cache. Scenario: load balancing across cache servers.", "Use hash ring with virtual nodes. On addition/removal, redistribute minimal keys. Use binary search for node lookup. Handle hot spots."),
    ("Design system for real-time analytics with window functions. Scenario: computing moving averages. Data structures.", "Use deque for sliding window. Calculate sum incrementally on add/remove. Handle window size changes. O(1) per update."),
    ("Find minimum insertions to form palindrome. Scenario: making string palindromic with insertions. DP approach.", "Find LPS (Longest Palindromic Subsequence). Insertions = n - LPS length. DP for LPS: LCS of string and reverse. O(n²)."),
]

new_questions = []
base_id = 20001

for q, a in easy_scenarios:
    new_questions.append({
        'id': base_id + len(new_questions),
        'topic': 'DSA',
        'question': q,
        'answer': a,
        'difficulty': 'Easy'
    })

for q, a in medium_scenarios:
    new_questions.append({
        'id': base_id + len(new_questions),
        'topic': 'DSA',
        'question': q,
        'answer': a,
        'difficulty': 'Medium'
    })

for q, a in hard_scenarios:
    new_questions.append({
        'id': base_id + len(new_questions),
        'topic': 'DSA',
        'question': q,
        'answer': a,
        'difficulty': 'Hard'
    })

questions.extend(new_questions)

with open('questions.json', 'w') as f:
    json.dump(questions, f, indent=2)

print(f'Added {len(new_questions)} unique DSA questions')
print(f'Total: {len(questions)}')

dsa_easy = len([q for q in questions if q.get('topic') == 'DSA' and q.get('difficulty') == 'Easy'])
dsa_medium = len([q for q in questions if q.get('topic') == 'DSA' and q.get('difficulty') == 'Medium'])
dsa_hard = len([q for q in questions if q.get('topic') == 'DSA' and q.get('difficulty') == 'Hard'])
print(f'DSA - Easy: {dsa_easy}, Medium: {dsa_medium}, Hard: {dsa_hard}')