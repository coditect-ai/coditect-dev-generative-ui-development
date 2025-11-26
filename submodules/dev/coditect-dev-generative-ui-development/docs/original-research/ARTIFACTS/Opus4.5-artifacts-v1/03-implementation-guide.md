# Generative UI Implementation Guide

*Production code templates and integration patterns*

---

## 1. React Component Templates

### 1.1 Accessible Button Component

```tsx
import React, { forwardRef } from "react";

type ButtonVariant = "primary" | "secondary" | "ghost";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  fullWidth?: boolean;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const sizeStyles: Record<ButtonSize, string> = {
  sm: "px-3 py-1.5 text-sm min-h-[36px]",
  md: "px-4 py-2 text-base min-h-[44px]",
  lg: "px-6 py-3 text-lg min-h-[52px]",
};

const variantStyles: Record<ButtonVariant, string> = {
  primary:
    "bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500",
  secondary:
    "bg-white text-slate-900 border border-slate-300 hover:bg-slate-50 focus-visible:ring-slate-500",
  ghost:
    "bg-transparent text-slate-700 hover:bg-slate-100 focus-visible:ring-slate-500",
};

const Spinner: React.FC<{ className?: string }> = ({ className }) => (
  <svg
    className={`animate-spin ${className}`}
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    aria-hidden="true"
  >
    <circle
      className="opacity-25"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="4"
    />
    <path
      className="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
    />
  </svg>
);

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = "primary",
      size = "md",
      fullWidth = false,
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      className = "",
      type = "button",
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || isLoading;

    return (
      <button
        ref={ref}
        type={type}
        disabled={isDisabled}
        aria-busy={isLoading}
        aria-disabled={isDisabled}
        className={`
          inline-flex items-center justify-center gap-2
          font-medium rounded-lg transition-colors duration-150
          focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
          disabled:opacity-50 disabled:cursor-not-allowed
          ${sizeStyles[size]}
          ${variantStyles[variant]}
          ${fullWidth ? "w-full" : ""}
          ${className}
        `}
        {...props}
      >
        {isLoading ? (
          <Spinner className="h-4 w-4" />
        ) : (
          leftIcon && (
            <span className="shrink-0" aria-hidden="true">
              {leftIcon}
            </span>
          )
        )}
        <span>{children}</span>
        {rightIcon && !isLoading && (
          <span className="shrink-0" aria-hidden="true">
            {rightIcon}
          </span>
        )}
      </button>
    );
  }
);

Button.displayName = "Button";
```

### 1.2 Product Grid Component

```tsx
import React from "react";

interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
  category: string;
}

interface ProductGridProps {
  products: Product[];
  onProductClick?: (productId: string) => void;
  emptyMessage?: string;
}

const formatPrice = (price: number): string =>
  price.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
  });

const ProductCard: React.FC<{
  product: Product;
  onClick?: () => void;
}> = ({ product, onClick }) => (
  <article
    className="
      group rounded-lg border border-slate-200 bg-white shadow-sm
      hover:shadow-md transition-shadow duration-200
      focus-within:ring-2 focus-within:ring-blue-500
    "
  >
    <div className="aspect-[4/3] overflow-hidden rounded-t-lg">
      <img
        src={product.imageUrl}
        alt={product.name}
        className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
        loading="lazy"
      />
    </div>
    <div className="p-4 flex flex-col gap-2">
      <span className="inline-flex self-start px-2 py-0.5 text-xs font-medium rounded-full bg-slate-100 text-slate-600">
        {product.category}
      </span>
      <h3 className="text-base font-semibold text-slate-900 line-clamp-2">
        {product.name}
      </h3>
      <p className="text-lg font-bold text-blue-600">
        {formatPrice(product.price)}
      </p>
      {onClick && (
        <button
          type="button"
          onClick={onClick}
          className="
            mt-2 inline-flex items-center justify-center
            rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white
            hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2
            focus-visible:ring-blue-500 focus-visible:ring-offset-2
            transition-colors duration-150
          "
        >
          View Details
        </button>
      )}
    </div>
  </article>
);

export const ProductGrid: React.FC<ProductGridProps> = ({
  products,
  onProductClick,
  emptyMessage = "No products found",
}) => {
  if (products.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <p className="text-slate-500 text-lg">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div
      className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
      role="list"
      aria-label="Products"
    >
      {products.map((product) => (
        <div key={product.id} role="listitem">
          <ProductCard
            product={product}
            onClick={onProductClick ? () => onProductClick(product.id) : undefined}
          />
        </div>
      ))}
    </div>
  );
};
```

### 1.3 Search Bar with Debounce

```tsx
import React, { useState, useEffect, useCallback, useRef } from "react";

interface SearchBarProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  debounceMs?: number;
  initialValue?: string;
  isLoading?: boolean;
}

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  placeholder = "Search...",
  onSearch,
  debounceMs = 300,
  initialValue = "",
  isLoading = false,
}) => {
  const [query, setQuery] = useState(initialValue);
  const debouncedQuery = useDebounce(query, debounceMs);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    onSearch(debouncedQuery);
  }, [debouncedQuery, onSearch]);

  const handleClear = useCallback(() => {
    setQuery("");
    inputRef.current?.focus();
  }, []);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      onSearch(query);
    },
    [query, onSearch]
  );

  return (
    <form
      onSubmit={handleSubmit}
      role="search"
      className="relative w-full max-w-lg"
    >
      <div className="relative flex items-center">
        <svg
          className="absolute left-3 h-5 w-5 text-slate-400 pointer-events-none"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
            clipRule="evenodd"
          />
        </svg>

        <input
          ref={inputRef}
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          aria-label={placeholder}
          className="
            w-full pl-10 pr-10 py-2.5
            border border-slate-300 rounded-lg
            text-slate-900 placeholder:text-slate-400
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
            transition-shadow duration-150
          "
        />

        {isLoading && (
          <svg
            className="absolute right-3 h-5 w-5 text-slate-400 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        )}

        {query && !isLoading && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute right-3 p-0.5 text-slate-400 hover:text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
            aria-label="Clear search"
          >
            <svg
              className="h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
            </svg>
          </button>
        )}
      </div>
    </form>
  );
};
```

---

## 2. Animated Components with Framer Motion

### 2.1 Motion Tokens

```tsx
// motion-tokens.ts
export const motionTokens = {
  duration: {
    instant: 0,
    fast: 0.12,
    normal: 0.24,
    slow: 0.4,
    slower: 0.6,
  },
  easing: {
    linear: [0, 0, 1, 1],
    easeOut: [0.16, 1, 0.3, 1],
    easeIn: [0.4, 0, 1, 1],
    easeInOut: [0.65, 0, 0.35, 1],
    spring: { type: "spring", stiffness: 400, damping: 30 },
  },
  distance: {
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
} as const;

export const transitions = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
    transition: { duration: motionTokens.duration.normal },
  },
  slideUp: {
    initial: { opacity: 0, y: motionTokens.distance.md },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -motionTokens.distance.sm },
    transition: {
      duration: motionTokens.duration.normal,
      ease: motionTokens.easing.easeOut,
    },
  },
  slideRight: {
    initial: { opacity: 0, x: -motionTokens.distance.lg },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: motionTokens.distance.lg },
    transition: {
      duration: motionTokens.duration.normal,
      ease: motionTokens.easing.easeOut,
    },
  },
  scale: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.95 },
    transition: {
      duration: motionTokens.duration.normal,
      ease: motionTokens.easing.easeOut,
    },
  },
};
```

### 2.2 Animated Card Component

```tsx
import React from "react";
import { motion, useReducedMotion } from "framer-motion";
import { motionTokens, transitions } from "./motion-tokens";

interface AnimatedCardProps {
  children: React.ReactNode;
  delay?: number;
  className?: string;
}

export const AnimatedCard: React.FC<AnimatedCardProps> = ({
  children,
  delay = 0,
  className = "",
}) => {
  const prefersReducedMotion = useReducedMotion();

  if (prefersReducedMotion) {
    return (
      <div
        className={`bg-white rounded-xl shadow-sm border border-slate-200 ${className}`}
      >
        {children}
      </div>
    );
  }

  return (
    <motion.div
      initial={transitions.slideUp.initial}
      animate={transitions.slideUp.animate}
      exit={transitions.slideUp.exit}
      transition={{
        ...transitions.slideUp.transition,
        delay,
      }}
      whileHover={{
        y: -4,
        boxShadow: "0 10px 40px -10px rgba(0, 0, 0, 0.15)",
        transition: { duration: motionTokens.duration.fast },
      }}
      className={`bg-white rounded-xl shadow-sm border border-slate-200 ${className}`}
    >
      {children}
    </motion.div>
  );
};
```

### 2.3 Onboarding Flow with Animations

```tsx
import React, { useState, useCallback, useEffect, useRef } from "react";
import { motion, AnimatePresence, useReducedMotion } from "framer-motion";

interface OnboardingStep {
  id: string;
  title: string;
  description: string;
  illustration?: React.ReactNode;
}

interface OnboardingFlowProps {
  steps: OnboardingStep[];
  onComplete: () => void;
  onSkip?: () => void;
}

const slideVariants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 100 : -100,
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction: number) => ({
    x: direction < 0 ? 100 : -100,
    opacity: 0,
  }),
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

export const OnboardingFlow: React.FC<OnboardingFlowProps> = ({
  steps,
  onComplete,
  onSkip,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [direction, setDirection] = useState(0);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const prefersReducedMotion = useReducedMotion();

  const currentStep = steps[currentIndex];
  const isFirstStep = currentIndex === 0;
  const isLastStep = currentIndex === steps.length - 1;

  useEffect(() => {
    headingRef.current?.focus();
  }, [currentIndex]);

  const goToNext = useCallback(() => {
    if (isLastStep) {
      onComplete();
    } else {
      setDirection(1);
      setCurrentIndex((prev) => prev + 1);
    }
  }, [isLastStep, onComplete]);

  const goToPrevious = useCallback(() => {
    if (!isFirstStep) {
      setDirection(-1);
      setCurrentIndex((prev) => prev - 1);
    }
  }, [isFirstStep]);

  const animationProps = prefersReducedMotion
    ? {}
    : {
        variants: slideVariants,
        custom: direction,
        initial: "enter",
        animate: "center",
        exit: "exit",
        transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
      };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Progress indicator */}
        <div className="mb-8" role="progressbar" aria-valuenow={currentIndex + 1} aria-valuemin={1} aria-valuemax={steps.length}>
          <div className="flex gap-2">
            {steps.map((step, index) => (
              <motion.div
                key={step.id}
                className={`h-1 flex-1 rounded-full ${
                  index <= currentIndex ? "bg-blue-600" : "bg-slate-200"
                }`}
                initial={false}
                animate={{
                  scaleX: index <= currentIndex ? 1 : 0.5,
                  opacity: index <= currentIndex ? 1 : 0.5,
                }}
                transition={{ duration: 0.3 }}
              />
            ))}
          </div>
          <p className="text-sm text-slate-500 mt-2 text-center">
            Step {currentIndex + 1} of {steps.length}
          </p>
        </div>

        {/* Step content */}
        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
          <AnimatePresence mode="wait" custom={direction}>
            <motion.div
              key={currentStep.id}
              {...animationProps}
              className="p-8"
            >
              <motion.div
                variants={prefersReducedMotion ? {} : staggerContainer}
                initial="initial"
                animate="animate"
              >
                {currentStep.illustration && (
                  <motion.div
                    variants={prefersReducedMotion ? {} : fadeInUp}
                    className="mb-6 flex justify-center"
                  >
                    {currentStep.illustration}
                  </motion.div>
                )}

                <motion.h2
                  ref={headingRef}
                  tabIndex={-1}
                  variants={prefersReducedMotion ? {} : fadeInUp}
                  className="text-2xl font-bold text-slate-900 text-center mb-4 focus:outline-none"
                >
                  {currentStep.title}
                </motion.h2>

                <motion.p
                  variants={prefersReducedMotion ? {} : fadeInUp}
                  className="text-slate-600 text-center leading-relaxed"
                >
                  {currentStep.description}
                </motion.p>
              </motion.div>
            </motion.div>
          </AnimatePresence>

          {/* Navigation */}
          <div className="px-8 pb-8 flex gap-3">
            {!isFirstStep && (
              <button
                type="button"
                onClick={goToPrevious}
                className="flex-1 px-4 py-3 rounded-lg border border-slate-300 text-slate-700 font-medium hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 transition-colors"
              >
                Back
              </button>
            )}
            <button
              type="button"
              onClick={goToNext}
              className="flex-1 px-4 py-3 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-colors"
            >
              {isLastStep ? "Get Started" : "Next"}
            </button>
          </div>
        </div>

        {/* Skip button */}
        {onSkip && !isLastStep && (
          <button
            type="button"
            onClick={onSkip}
            className="w-full mt-4 py-2 text-sm text-slate-500 hover:text-slate-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded transition-colors"
          >
            Skip onboarding
          </button>
        )}
      </div>
    </div>
  );
};
```

---

## 3. Multi-Step Form Wizard

```tsx
import React, { useState, useCallback, useRef, useEffect } from "react";

interface WizardStep {
  id: string;
  title: string;
  validate?: (data: Record<string, unknown>) => string | null;
}

interface WizardProps {
  steps: WizardStep[];
  onComplete: (data: Record<string, unknown>) => void;
  renderStep: (
    step: WizardStep,
    data: Record<string, unknown>,
    updateData: (updates: Record<string, unknown>) => void
  ) => React.ReactNode;
}

export const Wizard: React.FC<WizardProps> = ({
  steps,
  onComplete,
  renderStep,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [data, setData] = useState<Record<string, unknown>>({});
  const [error, setError] = useState<string | null>(null);
  const errorRef = useRef<HTMLDivElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);

  const currentStep = steps[currentIndex];
  const isFirstStep = currentIndex === 0;
  const isLastStep = currentIndex === steps.length - 1;
  const progress = ((currentIndex + 1) / steps.length) * 100;

  useEffect(() => {
    headingRef.current?.focus();
  }, [currentIndex]);

  useEffect(() => {
    if (error) {
      errorRef.current?.focus();
    }
  }, [error]);

  const updateData = useCallback((updates: Record<string, unknown>) => {
    setData((prev) => ({ ...prev, ...updates }));
    setError(null);
  }, []);

  const goToNext = useCallback(() => {
    if (currentStep.validate) {
      const validationError = currentStep.validate(data);
      if (validationError) {
        setError(validationError);
        return;
      }
    }

    if (isLastStep) {
      onComplete(data);
    } else {
      setCurrentIndex((prev) => prev + 1);
      setError(null);
    }
  }, [currentStep, data, isLastStep, onComplete]);

  const goToPrevious = useCallback(() => {
    if (!isFirstStep) {
      setCurrentIndex((prev) => prev - 1);
      setError(null);
    }
  }, [isFirstStep]);

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-lg bg-white rounded-xl shadow-lg border border-slate-200">
        {/* Progress bar */}
        <div className="p-6 border-b border-slate-200">
          <div
            className="h-2 bg-slate-200 rounded-full overflow-hidden"
            role="progressbar"
            aria-valuenow={currentIndex + 1}
            aria-valuemin={1}
            aria-valuemax={steps.length}
            aria-label={`Step ${currentIndex + 1} of ${steps.length}`}
          >
            <div
              className="h-full bg-blue-600 transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-slate-500 mt-2">
            Step {currentIndex + 1} of {steps.length}
          </p>
        </div>

        {/* Step content */}
        <div className="p-6">
          <h2
            ref={headingRef}
            tabIndex={-1}
            className="text-xl font-bold text-slate-900 mb-6 focus:outline-none"
          >
            {currentStep.title}
          </h2>

          {error && (
            <div
              ref={errorRef}
              role="alert"
              aria-live="polite"
              tabIndex={-1}
              className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm focus:outline-none"
            >
              {error}
            </div>
          )}

          {renderStep(currentStep, data, updateData)}
        </div>

        {/* Navigation */}
        <div className="p-6 border-t border-slate-200 flex gap-3">
          {!isFirstStep && (
            <button
              type="button"
              onClick={goToPrevious}
              className="flex-1 px-4 py-2.5 rounded-lg border border-slate-300 text-slate-700 font-medium hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 transition-colors"
            >
              Previous
            </button>
          )}
          <button
            type="button"
            onClick={goToNext}
            className="flex-1 px-4 py-2.5 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-colors"
          >
            {isLastStep ? "Complete" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

## 4. Dashboard Layout

```tsx
import React, { useState, useCallback } from "react";

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  href: string;
}

interface DashboardLayoutProps {
  navItems: NavItem[];
  activeItemId: string;
  onNavItemClick: (id: string) => void;
  logo: React.ReactNode;
  userMenu: React.ReactNode;
  children: React.ReactNode;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  navItems,
  activeItemId,
  onNavItemClick,
  logo,
  userMenu,
  children,
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const toggleSidebar = useCallback(() => {
    setSidebarOpen((prev) => !prev);
  }, []);

  const toggleCollapse = useCallback(() => {
    setSidebarCollapsed((prev) => !prev);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 z-50 h-full bg-white border-r border-slate-200
          transform transition-all duration-300 ease-in-out
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}
          lg:translate-x-0
          ${sidebarCollapsed ? "lg:w-20" : "lg:w-64"}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="h-16 flex items-center justify-between px-4 border-b border-slate-200">
            {!sidebarCollapsed && logo}
            <button
              type="button"
              onClick={toggleCollapse}
              className="hidden lg:flex p-2 rounded-lg text-slate-500 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
              aria-label={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d={sidebarCollapsed ? "M13 5l7 7-7 7M5 5l7 7-7 7" : "M11 19l-7-7 7-7m8 14l-7-7 7-7"}
                />
              </svg>
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 py-4 overflow-y-auto" aria-label="Main navigation">
            <ul className="space-y-1 px-3">
              {navItems.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => onNavItemClick(item.id)}
                    aria-current={activeItemId === item.id ? "page" : undefined}
                    className={`
                      w-full flex items-center gap-3 px-3 py-2.5 rounded-lg
                      text-sm font-medium transition-colors
                      focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500
                      ${
                        activeItemId === item.id
                          ? "bg-blue-50 text-blue-700"
                          : "text-slate-600 hover:bg-slate-100"
                      }
                    `}
                  >
                    <span className="shrink-0">{item.icon}</span>
                    {!sidebarCollapsed && <span>{item.label}</span>}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </aside>

      {/* Main content */}
      <div className={`lg:pl-${sidebarCollapsed ? "20" : "64"} transition-all duration-300`}>
        {/* Top bar */}
        <header className="sticky top-0 z-30 h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 lg:px-6">
          <button
            type="button"
            onClick={toggleSidebar}
            className="lg:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
            aria-label="Toggle sidebar"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <div className="flex-1" />

          {userMenu}
        </header>

        {/* Page content */}
        <main className="p-4 lg:p-6">{children}</main>
      </div>
    </div>
  );
};
```

---

## 5. HTML/CSS Templates

### 5.1 Standalone Search Bar

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Search Bar Component</title>
  <style>
    :root {
      --color-primary: #2563eb;
      --color-primary-hover: #1d4ed8;
      --color-surface: #ffffff;
      --color-border: #e2e8f0;
      --color-text: #0f172a;
      --color-text-muted: #64748b;
      --radius-full: 9999px;
      --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f8fafc;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }

    .search-container {
      width: 100%;
      max-width: 480px;
    }

    .search-form {
      display: flex;
      align-items: stretch;
      background: var(--color-surface);
      border-radius: var(--radius-full);
      border: 1px solid var(--color-border);
      box-shadow: var(--shadow-md);
      overflow: hidden;
      transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .search-form:focus-within {
      border-color: var(--color-primary);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1), var(--shadow-md);
    }

    .search-input {
      flex: 1;
      border: none;
      padding: 0.875rem 1.25rem;
      font-size: 1rem;
      color: var(--color-text);
      background: transparent;
      outline: none;
    }

    .search-input::placeholder {
      color: var(--color-text-muted);
    }

    .search-button {
      border: none;
      background: var(--color-primary);
      color: white;
      padding: 0 1.5rem;
      font-size: 0.9375rem;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: background 0.15s ease;
    }

    .search-button:hover {
      background: var(--color-primary-hover);
    }

    .search-button:focus-visible {
      outline: 2px solid var(--color-primary);
      outline-offset: 2px;
    }

    .search-icon {
      width: 1.125rem;
      height: 1.125rem;
    }

    @media (max-width: 480px) {
      .search-button span {
        display: none;
      }
      .search-button {
        padding: 0 1rem;
      }
    }
  </style>
</head>
<body>
  <div class="search-container">
    <form class="search-form" role="search" action="/search" method="GET">
      <input
        type="search"
        name="q"
        class="search-input"
        placeholder="Search anything..."
        aria-label="Search"
        autocomplete="off"
      />
      <button type="submit" class="search-button">
        <svg class="search-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd"/>
        </svg>
        <span>Search</span>
      </button>
    </form>
  </div>
</body>
</html>
```

---

## 6. Integration Utilities

### 6.1 Reduced Motion Hook

```tsx
import { useState, useEffect } from "react";

export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(mediaQuery.matches);

    const handleChange = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  return prefersReducedMotion;
}
```

### 6.2 Focus Management Hook

```tsx
import { useRef, useEffect, useCallback } from "react";

export function useFocusManagement<T extends HTMLElement>() {
  const elementRef = useRef<T>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  const captureFocus = useCallback(() => {
    previousFocusRef.current = document.activeElement as HTMLElement;
    elementRef.current?.focus();
  }, []);

  const restoreFocus = useCallback(() => {
    previousFocusRef.current?.focus();
    previousFocusRef.current = null;
  }, []);

  return { elementRef, captureFocus, restoreFocus };
}
```

### 6.3 Debounce Hook

```tsx
import { useState, useEffect } from "react";

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

---

*Document Version: 1.0*
*Framework: React 18+, TypeScript 5+*
*Styling: Tailwind CSS 3+*
*Last Updated: November 2025*
