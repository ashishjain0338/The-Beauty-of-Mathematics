import imageio
filenames = ["delete/" + str(i) + ".png" for i in range(100)]
with imageio.get_writer('movie.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)