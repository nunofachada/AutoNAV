"""This module contains the plotting functions."""

import matplotlib.pyplot as plt
from numpy.typing import NDArray

from .metrics import compute_rmse


def plot_trajectories(
    ideal_trajectory: NDArray,
    estimated_trajectories: list[NDArray],
    a_i: NDArray,
    names_of_the_algorithms: list[str] = None,
) -> list:
    """This function plots the ideal and estimated trajectory for one or more algorithms.

    Args:
        ideal_trajectory: The ideal trajectory that the UAV is supposed to follow.
        estimated_trajectories: The estimated trajectory that the UAV followed using the GTRS algorithm.
        names_of_the_algorithms: The names of the algorithms in the same order as in estimated_trajectories.
        a_i: The position of the anchors.

    Returns:
        A list of Matplotlib Axes object containing the ideal and estimated trajectory comparison.
    """
    names_of_the_algorithms = ["GTRS", "WLS"]
    if len(estimated_trajectories) == len(names_of_the_algorithms):
        axes = []
        for j in range(len(estimated_trajectories)):
            plt.figure(j)  # New figure foreach algorithm
            ax = plt.axes(projection="3d")
            a_i_label = "a_i"
            for i in range(0, a_i.shape[1]):
                ax.plot3D(
                    a_i[0][i],
                    a_i[1][i],
                    a_i[2][i],
                    marker="s",
                    markersize=10,
                    markeredgecolor="black",
                    markerfacecolor="black",
                    label=a_i_label,
                )
                a_i_label = "_nolegend_"  # Legend only in the first iteration
            ax.plot3D(
                ideal_trajectory[:, 0],
                ideal_trajectory[:, 1],
                ideal_trajectory[:, 2],
                color="green",
                label="Ideal Trajectory",
                linewidth=3.0,
                alpha=0.7,
            )
            ax.plot3D(
                estimated_trajectories[j][:, 0],
                estimated_trajectories[j][:, 1],
                estimated_trajectories[j][:, 2],
                label="Estimated Trajectory " + names_of_the_algorithms[j],
                color="red",
                alpha=1.0,
            )
            ax.set_title("Estimated Trajectory " + names_of_the_algorithms[j])
            ax.set_xlabel("Width")
            ax.set_ylabel("Length")
            ax.legend()
            axes.append(ax)
        return axes
    else:
        raise ValueError(
            "The number of algorithms must be the same in estimated_trajectories and names_of_the_algorithms."
        )


def plot_rmse(
    estimated_trajectories: list[NDArray],
    true_trajectories: list[NDArray],
    names_of_the_algorithms: list[str] = None,
) -> NDArray:
    """This function plots the root mean squared error along the trajectory.

    Args:
       estimated_trajectories: The estimated trajectory that the UAV followed using the GTRS algorithm.
       true_trajectories: The true trajectory that the UAV followed.
       names_of_the_algorithms: The names of the algorithms in the same order as in estimated_trajectories.

    Returns:
        An NDArray object containing the RMSE comparison.
    """
    names_of_the_algorithms = ["GTRS", "WLS"]
    if len(estimated_trajectories) == len(true_trajectories):
        fig, axs = plt.subplots(len(estimated_trajectories), sharey=True)
        # Space between subplots
        fig.tight_layout(pad=5.0)
        for i in range(len(estimated_trajectories)):
            rmse = compute_rmse(estimated_trajectories[i][:, :], true_trajectories[i][:, :])
            axs[i].plot(rmse)
            axs[i].set_title("RMSE " + names_of_the_algorithms[i])
        for ax in axs.flat:
            ax.set(xlabel="Iteration", ylabel="RMSE")
        return axs
    else:
        raise ValueError(
            "The number of algorithms must be the same in estimated_trajectories and names_of_the_algorithms."
        )
