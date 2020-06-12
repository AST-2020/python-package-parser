class SVC:
    """C-Support Vector Classification.
    The implementation is based on libsvm. The fit time scales at least
    quadratically with the number of samples and may be impractical
    beyond tens of thousands of samples. For large datasets
    consider using :class:`sklearn.svm.LinearSVC` or
    :class:`sklearn.linear_model.SGDClassifier` instead, possibly after a
    :class:`sklearn.kernel_approximation.Nystroem` transformer.
    The multiclass support is handled according to a one-vs-one scheme.
    For details on the precise mathematical formulation of the provided
    kernel functions and how `gamma`, `coef0` and `degree` affect each
    other, see the corresponding section in the narrative documentation:
    :ref:`svm_kernels`.
    Read more in the :ref:`User Guide <svm_classification>`.
    Parameters
    ----------
    C : float, optional (default=1.0)
        Regularization parameter. The strength of the regularization is
        inversely proportional to C. Must be strictly positive. The penalty
        is a squared l2 penalty.
    kernel : string, optional (default='rbf')
        Specifies the kernel type to be used in the algorithm.
        It must be one of 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed' or
        a callable.
        If none is given, 'rbf' will be used. If a callable is given it is
        used to pre-compute the kernel matrix from data matrices; that matrix
        should be an array of shape ``(n_samples, n_samples)``.
    degree : int, optional (default=3)
        Degree of the polynomial kernel function ('poly').
        Ignored by all other kernels.
    gamma : {'scale', 'auto'} or float, optional (default='scale')
        Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.
        - if ``gamma='scale'`` (default) is passed then it uses
          1 / (n_features * X.var()) as value of gamma,
        - if 'auto', uses 1 / n_features.
        .. versionchanged:: 0.22
           The default value of ``gamma`` changed from 'auto' to 'scale'.
    coef0 : float, optional (default=0.0)
        Independent term in kernel function.
        It is only significant in 'poly' and 'sigmoid'.
    shrinking : boolean, optional (default=True)
        Whether to use the shrinking heuristic.
    probability : boolean, optional (default=False)
        Whether to enable probability estimates. This must be enabled prior
        to calling `fit`, will slow down that method as it internally uses
        5-fold cross-validation, and `predict_proba` may be inconsistent with
        `predict`. Read more in the :ref:`User Guide <scores_probabilities>`.
    tol : float, optional (default=1e-3)
        Tolerance for stopping criterion.
    cache_size : float, optional
        Specify the size of the kernel cache (in MB).
    class_weight : {dict, 'balanced'}, optional
        Set the parameter C of class i to class_weight[i]*C for
        SVC. If not given, all classes are supposed to have
        weight one.
        The "balanced" mode uses the values of y to automatically adjust
        weights inversely proportional to class frequencies in the input data
        as ``n_samples / (n_classes * np.bincount(y))``
    verbose : bool, default: False
        Enable verbose output. Note that this setting takes advantage of a
        per-process runtime setting in libsvm that, if enabled, may not work
        properly in a multithreaded context.
    max_iter : int, optional (default=-1)
        Hard limit on iterations within solver, or -1 for no limit.
    decision_function_shape : 'ovo', 'ovr', default='ovr'
        Whether to return a one-vs-rest ('ovr') decision function of shape
        (n_samples, n_classes) as all other classifiers, or the original
        one-vs-one ('ovo') decision function of libsvm which has shape
        (n_samples, n_classes * (n_classes - 1) / 2). However, one-vs-one
        ('ovo') is always used as multi-class strategy.
        .. versionchanged:: 0.19
            decision_function_shape is 'ovr' by default.
        .. versionadded:: 0.17
           *decision_function_shape='ovr'* is recommended.
        .. versionchanged:: 0.17
           Deprecated *decision_function_shape='ovo' and None*.
    break_ties : bool, optional (default=False)
        If true, ``decision_function_shape='ovr'``, and number of classes > 2,
        :term:`predict` will break ties according to the confidence values of
        :term:`decision_function`; otherwise the first class among the tied
        classes is returned. Please note that breaking ties comes at a
        relatively high computational cost compared to a simple predict.
        .. versionadded:: 0.22
    random_state : int, RandomState instance or None, optional (default=None)
        The seed of the pseudo random number generator used when shuffling
        the data for probability estimates. If int, random_state is the
        seed used by the random number generator; If RandomState instance,
        random_state is the random number generator; If None, the random
        number generator is the RandomState instance used by `np.random`.
    Attributes
    ----------
    support_ : array-like of shape (n_SV)
        Indices of support vectors.
    support_vectors_ : array-like of shape (n_SV, n_features)
        Support vectors.
    n_support_ : array-like, dtype=int32, shape = [n_class]
        Number of support vectors for each class.
    dual_coef_ : array, shape = [n_class-1, n_SV]
        Coefficients of the support vector in the decision function.
        For multiclass, coefficient for all 1-vs-1 classifiers.
        The layout of the coefficients in the multiclass case is somewhat
        non-trivial. See the section about multi-class classification in the
        SVM section of the User Guide for details.
    coef_ : array, shape = [n_class * (n_class-1) / 2, n_features]
        Weights assigned to the features (coefficients in the primal
        problem). This is only available in the case of a linear kernel.
        `coef_` is a readonly property derived from `dual_coef_` and
        `support_vectors_`.
    intercept_ : ndarray of shape (n_class * (n_class-1) / 2,)
        Constants in decision function.
    fit_status_ : int
        0 if correctly fitted, 1 otherwise (will raise warning)
    classes_ : array of shape (n_classes,)
        The classes labels.
    probA_ : array, shape = [n_class * (n_class-1) / 2]
    probB_ : array, shape = [n_class * (n_class-1) / 2]
        If `probability=True`, it corresponds to the parameters learned in
        Platt scaling to produce probability estimates from decision values.
        If `probability=False`, it's an empty array. Platt scaling uses the
        logistic function
        ``1 / (1 + exp(decision_value * probA_ + probB_))``
        where ``probA_`` and ``probB_`` are learned from the dataset [2]_. For
        more information on the multiclass case and training procedure see
        section 8 of [1]_.
    class_weight_ : ndarray of shape (n_class,)
        Multipliers of parameter C for each class.
        Computed based on the ``class_weight`` parameter.
    shape_fit_ : tuple of int of shape (n_dimensions_of_X,)
        Array dimensions of training vector ``X``.
    See also
    --------
    SVR
        Support Vector Machine for Regression implemented using libsvm.
    LinearSVC
        Scalable Linear Support Vector Machine for classification
        implemented using liblinear. Check the See also section of
        LinearSVC for more comparison element.
    References
    ----------
    .. [1] `LIBSVM: A Library for Support Vector Machines
        <http://www.csie.ntu.edu.tw/~cjlin/papers/libsvm.pdf>`_
    .. [2] `Platt, John (1999). "Probabilistic outputs for support vector
        machines and comparison to regularizedlikelihood methods."
        <http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.41.1639>`_
    """

    _impl = 'c_svc'

    def __init__(self, C=1.0, kernel='rbf', degree=3, gamma='scale',
                 coef0=0.0, shrinking=True, probability=False,
                 tol=1e-3, cache_size=200, class_weight=None,
                 verbose=False, max_iter=-1, decision_function_shape='ovr',
                 break_ties=False,
                 random_state=None):

        super().__init__(
            kernel=kernel, degree=degree, gamma=gamma,
            coef0=coef0, tol=tol, C=C, nu=0., shrinking=shrinking,
            probability=probability, cache_size=cache_size,
            class_weight=class_weight, verbose=verbose, max_iter=max_iter,
            decision_function_shape=decision_function_shape,
            break_ties=break_ties,
            random_state=random_state)


class nextClass:
    def second(self, C=1.0, kernel='rbf', degree=3, gamma='scale',
                 coef0=0.0, shrinking=True):
        pass
