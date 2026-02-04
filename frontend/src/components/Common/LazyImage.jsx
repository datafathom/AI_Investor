import React, { useState, useEffect, useRef } from 'react';

/**
 * LazyImage Component
 * Loads images only when they enter the viewport using Intersection Observer.
 */
const LazyImage = ({ src, alt, className, placeholder = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7' }) => {
    const [imageSrc, setImageSrc] = useState(placeholder);
    const [isLoaded, setIsLoaded] = useState(false);
    const imageRef = useRef();

    useEffect(() => {
        let observer;
        let didCancel = false;

        if (imageRef.current && imageSrc === placeholder) {
            if (IntersectionObserver) {
                observer = new IntersectionObserver(
                    entries => {
                        entries.forEach(entry => {
                            if (
                                !didCancel &&
                                (entry.isIntersecting || entry.intersectionRatio > 0)
                            ) {
                                setImageSrc(src);
                                observer.unobserve(imageRef.current);
                            }
                        });
                    },
                    {
                        threshold: 0.01,
                        rootMargin: '75%',
                    }
                );
                observer.observe(imageRef.current);
            } else {
                // Fallback for older browsers
                setImageSrc(src);
            }
        }

        return () => {
            didCancel = true;
            if (observer && observer.unobserve) {
                observer.unobserve(imageRef.current);
            }
        };
    }, [src, imageSrc, placeholder]);

    return (
        <img
            ref={imageRef}
            src={imageSrc}
            alt={alt}
            className={`${className} transition-opacity duration-500 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
            onLoad={() => setIsLoaded(true)}
            loading="lazy"
        />
    );
};

export default LazyImage;
