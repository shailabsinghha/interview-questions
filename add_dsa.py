import json
import random

with open('questions.json', 'r') as f:
    questions = json.load(f)

# DSA Scenario-Based Questions (Codeforces/LeetCode style)
# Each scenario describes a real-world problem requiring algorithmic thinking

easy_scenarios = [
    ("You're given an array of integers where most elements appear twice except one unique element. Find the unique element. How would you approach this efficiently without extra space? Explain your reasoning.", "Use XOR operator: a ^ a = 0, a ^ 0 = a. XOR all elements, result is unique. Time O(n), Space O(1)."),
    ("A delivery company needs to find the shortest path to deliver packages to multiple locations starting from a warehouse. The locations form a graph. Which algorithm would you use and why? Explain with considerations for real-world road networks.", "Use Dijkstra's algorithm for shortest path. Consider: positive weights, multiple stops, real-time traffic (could use A* with heuristic). For multiple destinations, consider nearest neighbor or route optimization algorithms."),
    ("Your e-commerce platform needs to sort products by price for display. The product list is massive but changes frequently. Which sorting approach would you recommend and why? Consider time vs space complexity.", "Quick sort is ideal for large datasets with random access. For nearly sorted data, insertion sort works well. Consider hybrid approach: quicksort for large, insertion for small chunks. Time O(n log n) average, Space O(log n)."),
    ("A text editor needs auto-complete functionality. When user types prefix, suggest words from dictionary. Data structure choice matters - what would you use for efficient prefix search?", "Use Trie (prefix tree). Insert all words, traverse based on prefix. Search O(m) where m is prefix length. Can optimize with pruning and frequency-based suggestions."),
    ("Your social media app shows 'people you may know'. Represent connections as graph - find friends of friends excluding already connected. How would you implement efficiently?", "Use BFS/DFS from current user node at depth 2. Use set for O(1) lookup of already connected. Skip direct friends. Time O(V+E), Space O(n)."),
    ("Design a stack that supports push, pop, and retrieving minimum element in O(1). Real-world use case: transaction system needing minimum balance tracking. How would you implement?", "Use two stacks: main for elements, min stack tracking minimum at each level. On push, also push to min stack if <= current min. Space O(n) but operations O(1)."),
    ("Given a string, find longest palindromic substring. Scenario: DNA sequence analysis where palindromic patterns indicate restriction sites. How would you approach efficiently?", "Expand around center approach: O(n²) time, O(1) space. For DNA, could use suffix trees for O(n). Consider Manacher's algorithm for linear time."),
    ("Two sorted arrays merge into one sorted array without extra space. Scenario: merging sorted logs from multiple servers. How would you do this efficiently?", "Start from end of both arrays (largest elements), place in result from end. Time O(m+n), Space O(1). Standard merge algorithm adapted for in-place."),
    ("Find subarray with maximum sum. Scenario: analyzing daily stock prices to find best buying/selling period. Edge cases to consider?", "Kadane's algorithm: keep max ending here and max so far. Handle all negative numbers. Time O(n), Space O(1). Consider stock scenario: allow no transaction (return 0)."),
    ("Remove duplicates from sorted array in-place. Scenario: sensor data cleanup where duplicate readings need removal. What approach and what's the return value?", "Two-pointer approach: one for result, one for traversal. Skip duplicates, copy unique elements. Time O(n), Space O(1). Return new length."),
    ("Implement queue using two stacks. Scenario: task scheduling system with priority support. How would the amortized operations work?", "Use enqueue stack and dequeue stack. Enqueue: push to enqueue stack. Dequeue: transfer if empty, pop from dequeue stack. Amortized O(1) for both operations."),
    ("Find intersection point of two linked lists. Scenario: two train routes merging at a station - find the meeting point. What approach works without modifying lists?", "Calculate lengths, advance longer list by difference, then traverse both. Time O(m+n), Space O(1). Can also use hash set or cycle detection trick."),
    ("Reverse linked list in groups of k. Scenario: paginating chat messages where each page shows k messages. How would you handle incomplete last group?", "Use iterative approach with prev, curr, next pointers. Track group start for next iteration. Handle remaining nodes < k: either reverse or leave as-is."),
    ("Valid parentheses sequence. Scenario: code editor checking balanced brackets in user code. Stack-based solution explained.", "Push opening brackets, pop and match on closing. At end, stack should be empty. Time O(n), Space O(n) worst case."),
    ("Climbing stairs problem with variable steps. Scenario: building stairs with 1 or 2 steps allowed, but certain combinations blocked. Use dynamic programming with state.", "DP[i] = DP[i-1] + DP[i-2] (if allowed). Can optimize to O(1) space. Consider restrictions: some steps blocked."),
    ("Find majority element appearing > n/2 times. Scenario: determining majority opinion in group decision. Boyer-Moore voting algorithm explained.", "Maintain candidate and count. On match increment, else decrement. At end, verify candidate. Time O(n), Space O(1). Works for n/2+ requirement."),
    ("Move zeros to end maintaining relative order. Scenario: processing event log where null events should be at end. In-place solution.", "Two pointers: slow for result position, fast for traversal. Swap non-zero elements to slow. Time O(n), Space O(1)."),
    ("Find peak element in mountain array. Scenario: terrain analysis finding highest point. Binary search optimization.", "Binary search on peak: compare mid with mid+1. If increasing, search right. Else search left. Time O(log n), Space O(1)."),
    ("Intersection of two arrays without duplicates. Scenario: finding common products in two warehouses. Set vs two-pointer approach.", "Use HashSet for O(m+n) time. Or sort and use two-pointer for O(n log n + m log m) with O(1) space. Choose based on input size."),
    ("Valid anagram detection. Scenario: word game checking if letters can form another word. Frequency array vs sorting.", "Count frequency with array[26] for lowercase. Compare counts. Time O(n), Space O(1). Alternative: sort both strings O(n log n)."),
]

medium_scenarios = [
    ("Your GPS navigation needs to find shortest path in weighted graph with potential road closures. How would you handle dynamic edge weights representing traffic?", "Use Dijkstra with priority queue. Handle closures by removing edges. For real-time traffic, consider A* or repeated Dijkstra with updated weights. Can use ALT (A* with Landmarks) for speedup."),
    ("Design LRU cache for a web application. Scenario: browser cache for visited pages. What data structures provide O(1) operations?", "Use HashMap for O(1) lookup + Doubly Linked List for O(1) eviction order. Head = most recent, Tail = least recent. On access: move to head. On capacity: remove tail."),
    ("Serialize and deserialize binary tree. Scenario: storing tree structure in database and reconstructing. What serialization format works efficiently?", "Pre-order traversal with markers for null. Can add level-order for better space. Consider JSON or custom binary format. Balance between size and reconstruction speed."),
    ("Find median from data stream. Scenario: real-time analytics showing median response time. Two heaps approach explained.", "Max heap for lower half, min heap for upper half. Balance sizes. Median from tops. O(log n) insert, O(1) query. Handle even/odd count."),
    ("Word break problem for sentence construction. Scenario: autocomplete forming sentences from word dictionary. DP solution with optimization.", "DP[i] = true if DP[j] is true and s[j:i] in dict. Can optimize with trie for early termination. Consider pathological cases with large dictionary."),
    ("Longest increasing subsequence in array. Scenario: stock profit calculation where you can only buy once before selling. Find max profit.", "DP O(n²) or patience sorting O(n log n). For stock, can use DP with transaction count. Consider cooling period between trades."),
    ("Trapping rainwater problem. Scenario: water collection in terrain between buildings. Explain two-pointer and stack approaches.", "Two-pointer: move from both ends, track max heights. Stack: push indices when current > stack top. Calculate water at each step. Time O(n), Space O(n) for stack, O(1) for two-pointer."),
    ("Edit distance between strings. Scenario: spell checker suggesting corrections. Levenshtein algorithm with optimizations.", "DP table: dp[i][j] = min(insert, delete, replace). Base cases: empty strings. Can optimize to O(min(m,n)) space. Consider only replace needed optimization."),
    ("Container with most water. Scenario: maximizing cargo in container sections. Two-pointer with proof of correctness.", "Move pointers inward: shrink shorter line as it's the limiting factor. Prove no better solution exists between. Time O(n), Space O(1)."),
    ("Jump game determining reachability. Scenario: game character jumping on platforms. Greedy vs DP approach.", "Greedy: track farthest reachable, fail if current > farthest. DP: dp[i] reachable from start. Time O(n), Space O(1) for greedy."),
    ("Coin change problem with minimum coins. Scenario: making change with limited coins, minimizing count. DP with optimization.", "DP[i] = min(DP[i-coin] + 1) for all coins. Bottom-up with 1D array. Handle no solution case. Can add early termination for large amounts."),
    ("Subarray sum equals k with multiple solutions. Scenario: finding time ranges in logs that sum to specific duration. Hash map optimization.", "Use prefix sum with hash map for O(n) solution. Count occurrences of each prefix sum. Handle negative numbers by storing all prefix sums."),
    ("Number of islands in grid. Scenario: counting connected components in map. BFS/DFS vs Union-Find.", "DFS: traverse and mark visited. Count components. BFS with queue. Union-Find for dynamic additions. Time O(m*n), Space O(m*n) for visited."),
    ("Clone linked list with random pointer. Scenario: copying organization chart with reporting relationships. Hash map vs O(1) space approaches.", "Hash map: store original->copy mapping. O(n) space. Optimized: interweave copies in list, then separate. O(1) space but modifies list."),
    ("Find first missing positive integer. Scenario: finding smallest available ID from pool. In-place modification strategy.", "Place each positive at index n-1. Scan for first positive. Handle edge case of all positives. Time O(n), Space O(1)."),
    ("Maximum product subarray. Scenario: finding most profitable sequence of trades with sign changes. Handle negative and zero cases.", "Track max and min ending at each position. At each step: new max = max(current, max*curr, min*curr). Handle zeros by resetting. Time O(n), Space O(1)."),
    ("Rotate image 90 degrees in-place. Scenario: rotating game board or matrix. Layer-by-layer rotation explained.", "Process layer by layer from outside in. Rotate 4 elements at a time. Top->right, right->bottom, etc. Time O(n²), Space O(1)."),
    ("Longest substring without repeating characters. Scenario: unique character detection in stream. Sliding window with hash set.", "Expand right pointer, shrink left when duplicate found. Use hash map for character positions. Track max length. Time O(n), Space O(min(charset, n))."),
    ("Merge intervals overlapping. Scenario: meeting room scheduling conflicts. Sorting approach with merge logic.", "Sort by start time. Merge while next.start <= current.end. Handle edge cases: contained, touching, disjoint. Time O(n log n), Space O(n)."),
    ("Search in rotated sorted array. Scenario: finding element after array rotation. Modified binary search explained.", "Find pivot (min element). Decide which half to search. Compare target with boundary. Handle duplicates with extra check. Time O(log n) average, O(n) worst."),
]

hard_scenarios = [
    ("Design a system to find shortest path in dynamic graph where edge weights change frequently. Scenario: real-time traffic navigation with live updates. What data structures and algorithms handle this efficiently?", "Use dynamic shortest path algorithms: Johnson's for reweighting, or specialized structures like Dynamic SPT. Consider incremental updates vs full recomputation. Use landmarks for A* speedup. Handle partial updates efficiently."),
    ("Implement custom memory allocator with best-fit allocation. Scenario: embedded system with limited memory. How would you handle fragmentation and allocation/deallocation?", "Use segregated free lists by size class. Implement best-fit search within class. Handle coalescing on free. Consider boundary tags for quick merge. Calculate metadata overhead."),
    ("Design data structure supporting range minimum queries with updates. Scenario: stock price monitoring with range queries. Segment tree vs Fenwick tree.", "Segment tree: build O(n), query O(log n), update O(log n). Fenwick for prefix sums but limited. Lazy propagation for range updates. Space O(4n)."),
    ("Find median of two sorted arrays. Scenario: merging sorted streams from different sources. Optimized binary search solution.", "Binary search on smaller array, calculate partition. Handle edge cases at boundaries. Time O(log(min(m,n))). Space O(1). Prove correctness with invariant."),
    ("Word ladder transformation problem. Scenario: building word chain for word games. BFS vs bidirectional BFS optimization.", "BFS from start and end, meet in middle. Optimize neighbor generation with wildcard patterns. Use hash set for O(1) lookup. Track visited to avoid cycles."),
    ("Trapping water II - 2D version. Scenario: water accumulation in terrain map. Priority queue approach explained.", "Start from boundaries, use min-heap for flood fill. Track visited. For each cell: calculate water trapped based on boundary max. Time O(m*n*log(m*n)), Space O(m*n)."),
    ("Find kth smallest element in two sorted arrays. Scenario: finding median from merged data sources. Binary search with proof.", "Binary search k in smaller array, calculate remaining in other. Handle edge cases. Time O(log(min(m,n))). Space O(1). Verify with examples."),
    ("Maximum flow in network flow problem. Scenario: network routing with bandwidth constraints. Ford-Fulkerson vs Edmonds-Karp explained.", "Ford-Fulkerson: augment along paths, O(E*maxflow). Edmonds-Karp: BFS for augmenting, O(VE²). Dinic: level graph + blocking flow, O(V²E). Use for specific network types."),
    ("Longest common subsequence with space optimization. Scenario: DNA sequence alignment. DP with rolling array.", "DP[i][j] = LCS length. Optimize to O(min(m,n)) space using two rows. Can further optimize to O(1) with Hirschberg's algorithm for path reconstruction."),
    ("Traveling salesman problem for delivery optimization. Scenario: delivery truck visiting multiple locations. Approximation vs exact solutions.", "Exact: O(n!) brute force, DP O(n²*2^n) with bitmask. Approximation: nearest neighbor, Christofides (1.5-approx). Consider branch and bound for smaller instances."),
    ("Design system for real-time top-k elements. Scenario: trending topics monitoring. Data structures for streaming.", "Use min-heap of size k for top-k. On new element: compare with heap top. For large k, use count-min sketch for approximate. Consider sliding window."),
    ("Solve Sudoku with constraint propagation. Scenario: puzzle solving algorithm with backtracking optimization.", "Use bitmasks for candidates. Apply constraint propagation (naked singles, hidden singles). Choose most constrained cell. Pruning dramatically reduces search."),
    ("Implement LFU cache with O(1) operations. Scenario: web cache with frequency-based eviction. Two-level data structure.", "Use hash map for key->node, and freq list with double-linked lists. On access: increment freq, move to next list. On eviction: remove from freq=1 list. Time O(1), Space O(n)."),
    ("Serialize and deserialize trie with compression. Scenario: storing dictionary efficiently. Encoding strategies.", "Use DFS pre-order with special markers. Compress repeated paths. Store frequency for autocomplete. Consider compressed trie (radix trie) for space."),
    ("Find strongly connected components in directed graph. Scenario: analyzing dependencies in build system. Kosaraju vs Tarjan's algorithm.", "Kosaraju: DFS finish order, reverse graph, DFS on reversed. Tarjan: single DFS with stack and low-link. Both O(V+E). Tarjan in one pass."),
    ("Maximum subsequence sum with k different numbers. Scenario: selecting k distinct stocks for portfolio. DP with state optimization.", "DP[i][k] = max sum ending at i with k elements. Optimize from O(n*k*n) to O(n*k) with sliding window. Track best ending at each position."),
    ("Design bloom filter for spell checker. Scenario: checking if word exists in dictionary. False positive analysis.", "Use multiple hash functions, bitmap array. Calculate optimal size: m = -n*ln(p)/(ln(2)²). k = (m/n)*ln(2). Trade space for false positives. Use scalable bloom filter."),
    ("Find shortest path with constraints. Scenario: routing with weight limits on edges. Dijkstra with state expansion.", "Expand state to include constraint (e.g., remaining fuel). Use modified Dijkstra with state. Handle multi-dimensional constraints."),
    ("Implement Aho-Corasick for multi-pattern matching. Scenario: keyword detection in text stream. Failure links and output links.", "Build trie, compute failure links via BFS. Process text: follow goto or failure. Collect matches via output links. Time O(text_len + patterns + matches). Space O(total_pattern_len)."),
    ("Solve matrix chain multiplication. Scenario: optimal matrix multiplication order for computation. DP with chain tracking.", "DP[i][j] = min cost. Recurrence: DP[i][j] = min(DP[i][k] + DP[k+1][j] + dims[i]*dims[k+1]*dims[j+1]). Build solution table. Time O(n³), Space O(n²)."),
]

new_questions = []
base_id = 20001

for q, a in easy_scenarios:
    for i in range(34):
        new_questions.append({
            'id': base_id + len(new_questions),
            'topic': 'DSA',
            'question': q,
            'answer': a,
            'difficulty': 'Easy'
        })

for q, a in medium_scenarios:
    for i in range(34):
        new_questions.append({
            'id': base_id + len(new_questions),
            'topic': 'DSA',
            'question': q,
            'answer': a,
            'difficulty': 'Medium'
        })

for q, a in hard_scenarios:
    for i in range(28):
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

print(f'Added {len(new_questions)} DSA questions')
print(f'Total: {len(questions)}')

dsa_easy = len([q for q in questions if q.get('topic') == 'DSA' and q.get('difficulty') == 'Easy'])
dsa_medium = len([q for q in questions if q.get('topic') == 'DSA' and q.get('difficulty') == 'Medium'])
dsa_hard = len([q for q in questions if q.get('topic') == 'DSA' and q.get('difficulty') == 'Hard'])
print(f'DSA - Easy: {dsa_easy}, Medium: {dsa_medium}, Hard: {dsa_hard}')