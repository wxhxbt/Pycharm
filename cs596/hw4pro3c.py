import matplotlib.pyplot as plt
import numpy as np

scale = 10000
mu = 0.002
the_t = np.ones(5) * 7
theta = np.transpose(the_t)
th_prev_t = np.random.normal(0, 1, 5)
th_prev = np.transpose([th_prev_t])
record = np.zeros(scale)
for times in range(scale):
    Xt = np.random.normal(0, 1, 5)
    X = np.transpose([Xt])
    w = np.random.normal(0, np.sqrt(0.1))
    y = np.dot(the_t, X) + w
    th_cur = th_prev + mu * (y - np.dot(th_prev_t, X)) * X
    error = np.linalg.norm(th_cur - theta)**2
    th_prev = th_cur
    th_prev_t = np.transpose(th_prev)
    record[times] = error

mu = 0.002
record2 = np.zeros(scale)
th_prev_t = np.random.normal(0, 1, 5)
th_prev = np.transpose([th_prev_t])
for times in range(scale):
    Xt = np.random.normal(0, 1, 5)
    X = np.transpose([Xt])
    w = np.random.normal(0, np.sqrt(0.1))
    y = np.dot(the_t, X) + w
    th_cur = th_prev + mu * (y - np.dot(th_prev_t, X)) * X
    error = np.linalg.norm(th_cur - theta)**2
    th_prev = th_cur
    th_prev_t = np.transpose(th_prev)
    record2[times] = error

plt.figure()
plt.xlabel('t')
plt.ylabel('error')
# plt.plot(record, color='red', label='learning rate=0.004')
# plt.plot(record2, color='blue', linestyle='--', label='learning rate=0.002')
plt.plot(np.log(record), color='red', label='learning rate=0.004')
log1, log2 = np.log(record), np.log(record2)
print(np.average(log1[6000:10000]), np.average(log2[6000:10000]))
plt.plot(np.log(record2), color='blue', linestyle='--', label='learning rate=0.002')
plt.legend(loc='upper right')
plt.show()